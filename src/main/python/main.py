"""Entry point."""
import sys
import signal
from functools import partial
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from gust.gui.launcher import Launcher
import gust.server as server


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


if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    window = Launcher()
    window.show()

    register_sigterm(window)
    register_sigint(window)

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
