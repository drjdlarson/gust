import argparse
import os
import platform
from PyQt5.QtCore import QProcess

from gust.server.api.config import env_config
import gust.server.settings as settings
import gust.database as database


SERVER_PROC = None
PROGRAM = "gunicorn"
START_CMD = ''

_SERVER_RUNNING = False

_DB_CON_BASE_NAME = 'SERVER'
_SERVER_NUM = 0


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


def _build_db_con_name():
    global _DB_CON_BASE_NAME, _SERVER_NUM
    return '{:s}_{:02d}'.format(_DB_CON_BASE_NAME, _SERVER_NUM)

def start_server():
    global SERVER_PROC, START_CMD, PROGRAM, _SERVER_NUM, _SERVER_RUNNING

    if _SERVER_RUNNING:
        succ = False
        err = 'Server already started!!!'

    else:
        os.environ[settings.ENV_KEY] = settings.ENV

        if 'windows' in platform.system().lower():
            PROGRAM = "waitress-serve"
            args = ['--listen={:s}:{:d}'.format(settings.IP, settings.PORT),
                    '--threads={:d}'.format(settings.NUM_WORKERS),
                    'gust.server.wsgi:app']
        else:
            args = ['-b {:s}:{:d}'.format(settings.IP, settings.PORT),
                    '-w {:d}'.format(settings.NUM_WORKERS),
                    'gust.server.wsgi:app']

        SERVER_PROC = QProcess()
        SERVER_PROC.setProcessChannelMode(QProcess.MergedChannels)
        SERVER_PROC.start(PROGRAM, args)

        START_CMD = PROGRAM + ' ' + ' '.join(args)

        # succ, err = database.connect_to_database(con_name=_build_db_con_name())

        succ = _SERVER_RUNNING = True
        err = None

    _SERVER_NUM += 1

    return succ, err
    # return res, err


def stop_server():
    global SERVER_PROC, _SERVER_RUNNING

    succ = SERVER_PROC is not None and _SERVER_RUNNING
    if succ:
        # SERVER_PROC.terminate()
        SERVER_PROC.kill()
        SERVER_PROC.waitForBytesWritten(500)
        _SERVER_RUNNING = False  # SERVER_PROC still remains as an instance

    return succ
