"""Define functionality for the server."""
import platform
from PyQt5.QtCore import QProcess, QProcessEnvironment

import gust.server.settings as settings

__all__ = ['SERVER_PROC', 'START_CMD', 'start_server', 'stop_server']

SERVER_PROC = None
START_CMD = ''

_SERVER_RUNNING = False


def start_server(ctx):
    global SERVER_PROC, START_CMD, _SERVER_RUNNING

    if _SERVER_RUNNING:
        succ = False
        err = 'Server already started!!!'

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
        SERVER_PROC.start(program, args)

        START_CMD = program + ' ' + ' '.join(args)

        succ = _SERVER_RUNNING = True
        err = None

    return succ, err


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
