"""Helper functions for starting background worker threads."""
import sys
import traceback
import logging
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QObject


logger = logging.getLogger(__name__)

class WorkerSignals(QObject):
    """Defines the signals available from a running worker thread.

    Attributes
    ----------
    finished : pyqtSignal
        No data
    error : pyqtSignal
        tuple (exctype, value, traceback.format_exc() )
    result : pyqtSignal
        object data returned from processing, anything
    """

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class Worker(QRunnable):
    """Defines a worker for a thread.

    Create an instance of this class and pass the appropriate
    values to the constructor then pass the instance to a thread pools start
    function.
    """

    def __init__(self, fn, process_events, *args, **kwargs):
        super().__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.__process_events = process_events
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """Runs the specified function for the thread.

        This is required for the QRunnable object and should not need to be
        modified.

        Returns
        -------
        None.
        """
        try:
            result = self.fn(self.__process_events, *self.args, **self.kwargs)

        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
            logger.exception("Worker thread had an exception")

        else:
            self.signals.result.emit(result)  # Return the result of the processing

        finally:
            self.signals.finished.emit()  # Done
