"""Entry point."""
import os
import sys
import logging
import argparse
import signal
from functools import partial
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from gust.gui.launcher import Launcher
import gust.server.settings as server_settings
import gust.wsgi_apps.api.settings as api_settings
from gust.plugin_monitor import pluginMonitor


DAEMON = False

def parse_args():
    global DAEMON

    parser = argparse.ArgumentParser(description='Start the ground station backend.')

    msg = ('Environment to run the rest api app in. '
           + 'The default is {:s}'.format(api_settings.ENV))
    parser.add_argument('--api-env', type=str, help=msg, default=api_settings.ENV,
                        choices=api_settings.env_config.keys())

    msg = 'Flag indicating the server should start in the background with no GUI launcher'
    parser.add_argument('--daemon', '-d', action='store_true', help=msg)

    msg = ('Port number to listen on. '
           + 'The default is {:d}'.format(server_settings.PORT))
    parser.add_argument('--port', '-p',
                        help=msg, default=server_settings.PORT, type=int)

    msg = ('Number of worker threads to start for the server. '
           + 'The default is {:d}'.format(server_settings.NUM_WORKERS))
    parser.add_argument('--num-workers', help=msg, default=server_settings.NUM_WORKERS,
                        type=int)

    # %% Process input arguments
    args = parser.parse_args()

    server_settings.ENV = args.api_env
    DAEMON = args.daemon
    server_settings.PORT = args.port
    server_settings.NUM_WORKERS = args.num_workers


def sigterm_handler(signum, frame, app):
    app.close()


def sigint_handler(signum, frame, app):
    app.close()


def register_sigterm(app):
    global sigterm_handler
    handler = partial(sigterm_handler, app=app)
    signal.signal(signal.SIGTERM, handler)


def register_sigint(app):
    global sigint_handler
    handler = partial(sigint_handler, app=app)
    signal.signal(signal.SIGINT, handler)


def main():
    global DAEMON

    parse_args()

    if DAEMON:
        print('Not implemented yet!!')
        # server.start_server()
        sys.exit(1)

    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    window = Launcher(appctxt)
    window.show()

    register_sigterm(window)
    register_sigint(window)

    plug_readme = appctxt.get_resource('plugins/README.md')
    pluginMonitor.plugin_dir = os.path.dirname(plug_readme)

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)

# %% Start entry point
logging.basicConfig(level=logging.DEBUG)
main()
