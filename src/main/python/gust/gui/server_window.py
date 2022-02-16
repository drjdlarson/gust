"""Definition of the server window GUI."""
import sys
import os
import logging
import traceback
from functools import partial
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, QModelIndex, pyqtSignal, QRunnable, QThreadPool, QObject
from PyQt5.QtGui import QIntValidator, QTextCursor
from PyQt5.QtSql import QSqlTableModel

from gust.gui.ui.server_window import Ui_ServerWindow
import gust.server.server as server
import gust.server.settings as settings
from gust.plugins.plugin_monitor import pluginMonitor
import gust.database as database


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)

        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class ServerWindow(QMainWindow, Ui_ServerWindow):
    text_update = pyqtSignal(str)

    def __init__(self, ctx):
        super().__init__()
        self.setupUi(self)

        # setup redirect for stdout/stderr
        self.text_update.connect(self.update_console_text)
        sys.stdout = sys.stderr = self

        self.ctx = ctx
        self.lineEdit_port.setValidator(QIntValidator())
        self.threadpool = QThreadPool()

        settings.PORT = int(self.lineEdit_port.text())
        settings.IP = self.lineEdit_IP.text()

        # connect buttons
        self.pushButton_plugScan.clicked.connect(self.clicked_plugScan)
        self.pushButton_addPlugin.clicked.connect(self.clicked_addPlugin)
        self.pushButton_removePlugin.clicked.connect(self.clicked_removePlugin)
        self.pushButton_start.clicked.connect(self.clicked_start)
        self.pushButton_stop.clicked.connect(self.clicked_stop)
        self.lineEdit_IP.textChanged.connect(self.changed_ip)
        self.lineEdit_port.textChanged.connect(self.changed_port)

    def setup(self):
        self._scan_plugins()

        # connect to database
        database.DB_PATH = os.path.dirname(self.ctx.get_resource('resources_base_placeholder'))
        database.open_db()

        self.sel_plug_model = QSqlTableModel(self)
        self.sel_plug_model.setTable("PluginCollection")
        self.sel_plug_model.select()
        self.selPluginsView.setModel(self.sel_plug_model)
        self.selPluginsView.resizeColumnsToContents()

    def __del__(self):
        database.close_db()

    def _scan_plugins(self):
        pluginMonitor.scan_for_plugins()

        self.listWidget_availPlugins.clear()
        self.listWidget_availPlugins.addItems(pluginMonitor.avail_plugins)

        self.listWidget_availPlugins.sortItems()

    def setupUi(self, mainWindow):
        super().setupUi(mainWindow)

    def _stop_server(self):
        succ = server.stop_server()
        if not succ:
            msg = ('[server] Failed to stop server.')
            self.textEdit_output.append(msg)

        return succ

    def _stop_plug_mon(self):
        succ = pluginMonitor.stop_monitor()
        if not succ:
            msg = ('[plugin-monitor] Failed to stop plugin-monitor.')
            self.textEdit_output.append(msg)

        return succ

    def _stop_subtasks(self):
        succ = self._stop_server()
        succ = self._stop_plug_mon() and succ

        return succ

    # hacks for making the class behave like stdout and logging
    def write(self, text):
        self.text_update.emit(text)

    def flush(self):
        pass
    # end hacks

    def update_console_text(self, text):
        self.textEdit_output.moveCursor(QTextCursor.End)
        self.textEdit_output.insertPlainText(text)
        self.textEdit_output.moveCursor(QTextCursor.End)

    @pyqtSlot()
    def clicked_plugScan(self):
        self._scan_plugins()

    def _add_plugin(self, new_items):
        if len(new_items) > 0:
            new_items = [item.text() for item in new_items]
            for plugin_name in new_items:
                database.add_plugin(plugin_name)

    @pyqtSlot()
    def _update_sel_plug_model(self):
        self.sel_plug_model.setTable("PluginCollection")
        self.sel_plug_model.select()
        self.selPluginsView.resizeColumnsToContents()

    @pyqtSlot()
    def clicked_addPlugin(self):
        new_items = self.listWidget_availPlugins.selectedItems()

        worker = Worker(self._add_plugin, new_items)
        worker.signals.finished.connect(self._update_sel_plug_model)
        self.threadpool.start(worker)

    def _remove_plugin(self, rows_to_rm):
        n_to_rm = len(rows_to_rm)
        if n_to_rm > 0:
            col_ids_to_rm = [None] * n_to_rm
            c_ind = self.sel_plug_model.fieldIndex('collection_id')
            for ii, row in enumerate(rows_to_rm):
                ind = QModelIndex(self.sel_plug_model.index(row, c_ind))
                col_ids_to_rm[ii] = self.selPluginsView.model().data(ind)

            database.remove_plugin_by_col_id(col_ids_to_rm)

    @pyqtSlot()
    def clicked_removePlugin(self):
        rows_to_rm = set([index.row()
                          for index in self.selPluginsView.selectedIndexes()])

        worker = Worker(self._remove_plugin, rows_to_rm)
        worker.signals.finished.connect(self._update_sel_plug_model)
        self.threadpool.start(worker)

    # hacks to redirect from subprocess to stdout of main process
    def _sub_proc_print(self, line, prefix):
        line = line.strip('\n').strip()
        if len(line) == 0:
            return
        print('{:s} {:s}'.format(prefix, line.strip('\n')))

    def _print_server_proc_msg(self):
        outputBytes = server.SERVER_PROC.readAll().data()
        outputUnicode = outputBytes.decode('utf-8')
        for line in outputUnicode.split('\n'):
            self._sub_proc_print(line, '[server]')

    def _print_plug_msg(self, ind):
        outputBytes = pluginMonitor.running_procs[ind].readAll().data()
        outputUnicode = outputBytes.decode('utf-8')
        prefix = '[plugin-{:s}-{:s}]'.format(pluginMonitor.running_names[ind],
                                             pluginMonitor.running_ids[ind])
        for line in outputUnicode.split('\n'):
            self._sub_proc_print(line, prefix)
    # end hacks

    @pyqtSlot()
    def clicked_start(self):
        msg = ('----------------------------------------------------------\n'
               + '------------------- Starting Backend ---------------------\n'
               + '----------------------------------------------------------\n')
        self.update_console_text(msg)

        res, err = server.start_server()

        self.update_console_text('[server] {:s}\n'.format(server.START_CMD))

        if res:
            # pass
            server.SERVER_PROC.readyReadStandardOutput.connect(self._print_server_proc_msg)

        else:
            msg = '[server] FAILED TO START SERVER:\n{:s}\n'.format(err)
            self.update_console_text(msg)

        pluginMonitor.scan_for_plugins()
        pluginMonitor.start_monitor()
        for ii, proc in enumerate(pluginMonitor.running_procs):
            proc.readyReadStandardOutput.connect(partial(self._print_plug_msg, ii))

    @pyqtSlot()
    def clicked_stop(self):
        succ = self._stop_subtasks()

        if succ:
            msg = ('----------------------------------------------------------\n'
                  + '------------------- Stopping Backend ---------------------\n'
                  + '----------------------------------------------------------\n\n')
            self.update_console_text(msg)

    @pyqtSlot(str)
    def changed_ip(self, text):
        settings.IP = text

    @pyqtSlot(str)
    def changed_port(self, text):
        settings.PORT = int(text)

    def closeEvent(self, event):
        # nicely close all
        self._stop_subtasks()

        sys.stdout.flush()
        sys.stderr.flush()
