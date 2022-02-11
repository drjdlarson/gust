import argparse
import subprocess
import os
import atexit

from gust.server.api.config import env_config
import gust.server.settings as settings


SERVER_PROC = None

def parse_args(*args):

    parser = argparse.ArgumentParser(description='Start the ground station backend.')

    msg = ('Environment to run the server in. '
           + 'The default is {:s}'.format(settings.ENV))
    parser.add_argument('--env', type=str, help=msg, default=settings.ENV,
                        choices=env_config.keys())

    msg = 'Flag indicating the server should start in the background with no GUI launcher'
    parser.add_argument('--daemon', '-d', action='store_true', help=msg)

    msg = ('Port number to listen on. '
           + 'The default is {:d}'.format(settings.PORT))
    parser.add_argument('--port', '-p',
                        help=msg, default=settings.PORT, type=int)

    msg = ('Number of worker threads to start for the server. '
           + 'The default is {:d}'.format(settings.NUM_WORKERS))
    parser.add_argument('--num-workers', help=msg, default=settings.NUM_WORKERS,
                        type=int)

    # %% Process input arguments
    args = parser.parse_args()

    settings.ENV = args.env
    settings.DAEMON = args.daemon
    settings.PORT = args.port
    settings.NUM_WORKERS = args.num_workers


def start_server():
    global SERVER_PROC
    os.environ[settings.ENV_KEY] = settings.ENV

    # TODO: figure out what to do with stdout/err of subproc
    SERVER_PROC = subprocess.Popen(['gunicorn',
                                    '-b 127.0.0.1:{:d}'.format(settings.PORT),
                                    '-w {:d}'.format(settings.NUM_WORKERS),
                                    'gust.server.wsgi:app'])
