"""Define functionality for the server."""
import platform
import logging
from PyQt5.QtCore import QProcess, QProcessEnvironment

import gust.server.settings as settings

__all__ = ['SERVER_PROC', 'START_CMD', 'start_server', 'stop_server']

logger = logging.getLogger(__name__)
logger.propagate = False



SERVER_PROC = None
START_CMD = ''

_SERVER_RUNNING = False
_LOGGER_WAS_INITED = False


def start_server(ctx, debug):
    """Starting the main backend server process.
    This is started from the Backend window"""

    global SERVER_PROC, START_CMD, _SERVER_RUNNING, _LOGGER_WAS_INITED

    if not _LOGGER_WAS_INITED:
        ch = logging.StreamHandler()
        if debug:
            logger.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            ch.setLevel(logging.INFO)

        formatter = logging.Formatter('[server] %(levelname)s %(asctime)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        _LOGGER_WAS_INITED = True

    if _SERVER_RUNNING:
        logger.critical('Server already started!!!')

    else:
        if 'windows' in platform.system().lower():
            program = 'waitress-serve'
            raise RuntimeError("Windows is not supported yet!!")
            # args = ['--listen={:s}:{:d}'.format(settings.IP, settings.PORT),
            #         '--threads={:d}'.format(settings.NUM_WORKERS),
            #         _REST_API_APP]
        else:
            program = ctx.get_resource('wsgi_apps/wsgi_apps')
            args = [
                "--port",
                "{}".format(settings.PORT),
                "--ip",
                "{}".format(settings.IP),
                "--num-workers",
                "{}".format(settings.NUM_WORKERS),
            ]

        SERVER_PROC = QProcess()
        SERVER_PROC.setProcessChannelMode(QProcess.MergedChannels)
        SERVER_PROC.setProcessEnvironment(QProcessEnvironment.systemEnvironment())
        SERVER_PROC.readyRead.connect(lambda: print(SERVER_PROC.readAllStandardOutput().data().decode().strip()))
        START_CMD = program + ' ' + ' '.join(args)
        logger.info(START_CMD)
        SERVER_PROC.start(program, args)

        success = _SERVER_RUNNING = SERVER_PROC.waitForStarted(1000)
        if not success:
            logger.critical("Failed to start server")



def stop_server():
    """Stop the backend server process"""
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
