"""Logic for program launcher window."""
import sys
import logging
from queue import Queue
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal, QThread

from gust.gui.ui.launcher import Ui_Launcher
from gust.gui import backend_window
from gust.gui import frontend_window
from gust.gui import log_window
from gust import logger


# see https://stackoverflow.com/questions/21071448/redirecting-stdout-and-stderr-to-a-pyqt4-qtextedit-from-a-secondary-thread for below
# ---------------------------------------------------------------------------------------------------------------------------------------
# The new Stream Object which replaces the default stream associated with sys.stdout
# This object just puts data in a queue!
class WriteStream:
    def __init__(self, queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)

    def flush(self):
        pass


# A QObject (to be run in a QThread) which sits waiting for data to come through a Queue.Queue().
# It blocks until data is available, and one it has got something from the queue, it sends
# it to the "MainThread" by emitting a Qt Signal
class MyReceiver(QObject):
    mysignal = pyqtSignal(str)

    def __init__(self, queue, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.queue = queue

    @pyqtSlot()
    def run(self):
        while True:
            text = self.queue.get()
            self.mysignal.emit(text)


class Launcher(QMainWindow, Ui_Launcher):
    """Main program launcher Window"""

    def __init__(self, ctx, process_events, debug):
        super().__init__()
        self.ctx = ctx
        self.setupUi(self)

        self._debug = debug
        self.__process_events = process_events

        # connect buttons
        self.pushButton_client.clicked.connect(self.clicked_client)
        self.pushButton_server.clicked.connect(self.clicked_server)
        self.pushButton_log.clicked.connect(self.clicked_log)

        self._backendWindow = None
        self._frontendWindow = None
        self._logWindow = None
        self._std_thread = None
        self._std_receiver = None

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

    @pyqtSlot()
    def clicked_client(self):
        """Event connection for client. Opens up FrontendWindow"""
        self._frontendWindow = frontend_window.FrontendWindow(self.ctx)

        self._frontendWindow.show()
        self.close()

    @pyqtSlot()
    def clicked_server(self):
        """Event connection for server. Opens up BackendWindow"""
        # Create Queue and redirect sys.stdout to this queue
        q = Queue()
        sys.stdout = WriteStream(q)
        sys.stderr = WriteStream(q)

        ch = logging.StreamHandler(stream=sys.stdout)
        if self._debug:
            logger.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            ch.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[backend] %(levelname)s %(asctime)s - %(message)s"
        )

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        self._backendWindow = backend_window.BackendWindow(
            self.ctx, self.__process_events, self._debug
        )
        self._backendWindow.setup()
        self._backendWindow.show()

        self._std_thread = QThread()
        self._std_receiver = MyReceiver(q)
        self._std_receiver.mysignal.connect(self._backendWindow.update_console_text)
        self._std_receiver.moveToThread(self._std_thread)
        self._std_thread.started.connect(self._std_receiver.run)
        self._std_thread.start()

        self.close()

    @pyqtSlot()
    def clicked_log(self):
        """Event connection for log. Opens up the LogWindow"""
        self._logWindow = log_window.LogWindow(self.ctx)
        self._logWindow.show()
