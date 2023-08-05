# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os
import sys
import imp
import logging
from copy import deepcopy

from docopt import docopt
import botocore.session
from clint.textui import colored
from botocore.vendored import requests
from logging.config import dictConfig

from . import gcdt_signals
from .gcdt_defaults import DEFAULT_CONFIG
from .utils import get_context, check_gcdt_update, are_credentials_still_valid, \
    get_env
from .gcdt_cmd_dispatcher import cmd, get_command
from .gcdt_plugins import load_plugins
from .gcdt_awsclient import AWSClient
from .gcdt_logging import logging_config
from .gcdt_signals import check_hook_mechanism_is_intact, \
    check_register_present


log = logging.getLogger(__name__)


def check_vpn_connection(reposerver):
    """Check whether we can connect to VPN for version check.
    :return: True / False
    """
    try:
        request = requests.get(reposerver, timeout=1.0)
        if request.status_code == 200:
            return True
        else:
            return False
    except Exception:
        #requests.exceptions.ConnectTimeout:
        #requests.exceptions.ConnectionError
        return False


def _load_hooks(path):
    """Load hook module and register signals.

    :param path: Absolute or relative path to module.
    :return: module
    """
    module = imp.load_source(os.path.splitext(os.path.basename(path))[0], path)
    if not check_hook_mechanism_is_intact(module):
        # no hooks - do nothing
        log.debug('No valid hook configuration: \'%s\'. Not using hooks!', path)
    else:
        if check_register_present(module):
            # register the template hooks so they listen to gcdt_signals
            module.register()
    return module


# lifecycle implementation adapted from
# https://github.com/finklabs/aws-deploy/blob/master/aws_deploy/tool.py
def lifecycle(awsclient, env, tool, command, arguments):
    """Tool lifecycle which provides hooks into the different stages of the
    command execution. See signals for hook details.
    """
    load_plugins()
    context = get_context(awsclient, env, tool, command, arguments)
    # every tool needs a awsclient so we provide this via the context
    context['_awsclient'] = awsclient
    log.debug('### context:')
    log.debug(context)
    if 'error' in context:
        # no need to send an 'error' signal here
        return 1

    ## initialized
    gcdt_signals.initialized.send(context)
    check_gcdt_update()

    config = deepcopy(DEFAULT_CONFIG)
    # TODO move this to glomex-checks plugin!
    #if not check_vpn_connection(config['reposerver']):
    #    print(colored.red('Can not connect to VPN please activate your VPN!'))
    #    return 1

    gcdt_signals.config_read_init.send((context, config))
    gcdt_signals.config_read_finalized.send((context, config))
    # TODO we might want to be able to override config via env variables?
    # here would be the right place to do this
    if 'hookfile' in config:
        # load hooks from hookfile
        _load_hooks(config['hookfile'])

    ## lookup
    # credential retrieval should be done using lookups
    gcdt_signals.lookup_init.send((context, config))
    gcdt_signals.lookup_finalized.send((context, config))
    log.debug('### config after lookup:')
    log.debug(config)

    ## config validation
    gcdt_signals.config_validation_init.send((context, config))
    gcdt_signals.config_validation_finalized.send((context, config))

    ## check credentials are valid (AWS services)
    if are_credentials_still_valid(awsclient):
        context['error'] = \
            'Your credentials have expired... Please renew and try again!'
        log.error(context['error'])
        gcdt_signals.error.send((context, config))
        return 1

    ## bundle step
    gcdt_signals.bundle_pre.send((context, config))
    gcdt_signals.bundle_init.send((context, config))
    gcdt_signals.bundle_finalized.send((context, config))
    if 'error' in context:
        gcdt_signals.error.send((context, config))
        return 1

    ## dispatch command providing context and config (= tooldata)
    gcdt_signals.command_init.send((context, config))
    try:
        exit_code = cmd.dispatch(arguments,
                                 context=context,
                                 config=config[tool])
    except Exception as e:
        print(str(e))
        context['error'] = str(e)
        exit_code = 1
    if exit_code:
        gcdt_signals.error.send((context, config))
        return 1

    gcdt_signals.command_finalized.send((context, config))

    # TODO reporting (in case you want to get a summary / output to the user)

    gcdt_signals.finalized.send(context)
    return 0


def main(doc, tool, dispatch_only=None):
    """gcdt tools parametrized main function to initiate gcdt lifecycle.

    :param doc: docopt string
    :param tool: gcdt tool (gcdt, kumo, tenkai, ramuda, yugen)
    :return: exit_code
    """
    arguments = docopt(doc, sys.argv[1:])
    # DEBUG mode (if requested)
    verbose = arguments.pop('--verbose', False)
    if verbose:
        logging_config['loggers']['gcdt']['level'] = 'DEBUG'
    dictConfig(logging_config)

    env = get_env()
    if not env:
        log.error('\'ENV\' environment variable not set!')
        return 1

    if dispatch_only is None:
        dispatch_only = ['version']
    assert tool in ['gcdt', 'kumo', 'tenkai', 'ramuda', 'yugen']

    command = get_command(arguments)
    if command in dispatch_only:
        # handle commands that do not need a lifecycle
        check_gcdt_update()
        return cmd.dispatch(arguments)
    else:
        awsclient = AWSClient(botocore.session.get_session())
        return lifecycle(awsclient, env, tool, command, arguments)
