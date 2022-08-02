"""Helper functions for starting background worker threads."""
import sys
import traceback
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QObject


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

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
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
            result = self.fn(*self.args, **self.kwargs)
            print("trying in worker")

        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
            print("handling exception")
        else:
            self.signals.result.emit(result)  # Return the result of the processing
            print("else part")
        finally:
            self.signals.finished.emit()  # Done
            print("reached final part", flush=True)
