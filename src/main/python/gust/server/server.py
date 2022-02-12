"""Define functionality for the server."""
import platform
import os
from PyQt5.QtCore import QProcess

import gust.server.settings as settings
import gust.database as database
from gust.wsgi_apps.setup import initialize_environment as wsgi_init_environ

__all__ = ['SERVER_PROC', 'START_CMD', 'start_server', 'stop_server']

SERVER_PROC = None
START_CMD = ''

_SERVER_RUNNING = False

_DB_CON_BASE_NAME = 'SERVER'
_SERVER_NUM = 0

_REST_API_APP = 'gust.wsgi_apps.wsgi:rest_api'


def _build_db_con_name():
    global _DB_CON_BASE_NAME, _SERVER_NUM
    return '{:s}_{:02d}'.format(_DB_CON_BASE_NAME, _SERVER_NUM)


def start_server():
    global SERVER_PROC, START_CMD, _SERVER_NUM, _SERVER_RUNNING

    if _SERVER_RUNNING:
        succ = False
        err = 'Server already started!!!'

    else:
        wsgi_init_environ()

        if 'windows' in platform.system().lower():
            program = 'waitress-serve'
            args = ['--listen={:s}:{:d}'.format(settings.IP, settings.PORT),
                    '--threads={:d}'.format(settings.NUM_WORKERS),
                    _REST_API_APP]
        else:
            program = 'gunicorn'
            args = ['-b {:s}:{:d}'.format(settings.IP, settings.PORT),
                    '-w {:d}'.format(settings.NUM_WORKERS),
                    '--enable-stdio-inheritance',
                    _REST_API_APP]

        SERVER_PROC = QProcess()
        SERVER_PROC.setProcessChannelMode(QProcess.MergedChannels)
        SERVER_PROC.start(program, args)

        START_CMD = program + ' ' + ' '.join(args)

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
        if 'windows' in platform.system().lower():
            SERVER_PROC.kill()
        else:
            SERVER_PROC.terminate()

        SERVER_PROC.waitForFinished(1500)  # 1.5 sec timeout
        _SERVER_RUNNING = False  # SERVER_PROC still remains as an instance

    return succ
