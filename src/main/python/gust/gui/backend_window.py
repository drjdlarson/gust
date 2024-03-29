"""Definition of the server window GUI."""
import sys
import os
import logging

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSlot, QModelIndex, pyqtSignal, QThreadPool, QObject
from PyQt5.QtGui import QIntValidator, QTextCursor
from PyQt5.QtSql import QSqlTableModel

from gust.gui.ui.backend_window import Ui_BackendWindow
import gust.server.server as server
import gust.server.settings as settings
from gust.plugin_monitor import pluginMonitor
import utilities.database as database
from gust.worker import Worker
import gust.conn_manager.conn_server as conn_server

logger = logging.getLogger(__name__)


class BackendWindow(QMainWindow, Ui_BackendWindow):
    """Main interface for the backend window."""

    # signal to kill ConnServer's process once the backend is shut
    kill_conn_server_signal = pyqtSignal()

    def __init__(self, ctx, process_events, debug):
        super().__init__()
        self.setupUi(self)

        self.__process_events = process_events
        self._debug = debug

        self.ctx = ctx
        self.lineEdit_port.setValidator(QIntValidator())
        self.threadpool = QThreadPool()

        self.kill_conn_server_signal.connect(conn_server.ConnServer.kill)

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
        """Setup code for some of the backend elements.

        These can not be called from the constructor. Should be called once
        before the show function.

        Returns
        -------
        None.
        """
        self._scan_plugins()

        # connect to database
        database.set_db_path(
            os.path.dirname(self.ctx.get_resource("resources_base_placeholder"))
        )
        database.open_db(self.ctx.get_resource("locations.txt"))

        self.sel_plug_model = QSqlTableModel(self)
        self._update_sel_plug_model()
        self.selPluginsView.setModel(self.sel_plug_model)
        self.selPluginsView.setColumnHidden(0, True)

    def __del__(self):
        """Clean up things on delete.

        Returns
        -------
        None.
        """
        database.close_db()

    def _scan_plugins(self):
        """
        Scans and lists available plugins

        Returns
        -------

        """
        pluginMonitor.scan_for_plugins()

        self.listWidget_availPlugins.clear()
        self.listWidget_availPlugins.addItems(pluginMonitor.avail_plugins)

        self.listWidget_availPlugins.sortItems()

    def setupUi(self, mainWindow):
        """Sets up the user interface."""
        super().setupUi(mainWindow)

    def _stop_server(self):
        succ = server.stop_server()
        if not succ:
            logger.critical("Failed to stop server.")

        return succ

    def _stop_plug_mon(self):
        succ = pluginMonitor.stop_monitor()
        if not succ:
            logger.critical("Failed to stop plugin-monitor")

        return succ

    def _stop_subtasks(self):
        self.kill_conn_server_signal.emit()
        succ = self._stop_server()
        succ = self._stop_plug_mon() and succ
        return succ

    def update_console_text(self, text):
        """Update the console text."""
        self.textEdit_output.moveCursor(QTextCursor.End)
        self.textEdit_output.insertPlainText(text)
        self.textEdit_output.moveCursor(QTextCursor.End)

    @pyqtSlot()
    def clicked_plugScan(self):
        """Actions to perform when the scan button is clicked."""
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
        self.selPluginsView.setColumnHidden(0, True)
        self.selPluginsView.resizeColumnsToContents()

    @pyqtSlot()
    def clicked_addPlugin(self):
        """Actions to perform when the add button is clicked."""
        new_items = self.listWidget_availPlugins.selectedItems()

        worker = Worker(self._add_plugin, new_items)
        worker.signals.finished.connect(self._update_sel_plug_model)
        self.threadpool.start(worker)

    def _remove_plugin(self, rows_to_rm):
        n_to_rm = len(rows_to_rm)
        if n_to_rm > 0:
            col_ids_to_rm = [None] * n_to_rm
            c_ind = self.sel_plug_model.fieldIndex("collection_id")
            for ii, row in enumerate(rows_to_rm):
                ind = QModelIndex(self.sel_plug_model.index(row, c_ind))
                col_ids_to_rm[ii] = self.selPluginsView.model().data(ind)

            database.remove_plugin_by_col_id(col_ids_to_rm)

    @pyqtSlot()
    def clicked_removePlugin(self):
        """Actions to perform when the remove button is clicked."""
        rows_to_rm = set(
            [index.row() for index in self.selPluginsView.selectedIndexes()]
        )

        worker = Worker(self._remove_plugin, rows_to_rm)
        worker.signals.finished.connect(self._update_sel_plug_model)
        self.threadpool.start(worker)

    # hacks to redirect from subprocess to stdout of main process
    def _sub_proc_print(self, line, prefix):
        line = line.strip("\n").strip()
        if len(line) == 0:
            return
        print("{:s} {:s}".format(prefix, line.strip("\n")))

    def _print_plug_msg(self, ind):
        outputBytes = pluginMonitor.running_procs[ind].readAll().data()
        outputUnicode = outputBytes.decode("utf-8")
        prefix = "[plugin-{:s}-{:d}]".format(
            pluginMonitor.running_names[ind], pluginMonitor.running_ids[ind]
        )
        for line in outputUnicode.split("\n"):
            self._sub_proc_print(line, prefix)

    # end hacks

    @pyqtSlot()
    def clicked_start(self):
        """Actions to perform when the start button is clicked."""
        msg = (
            "----------------------------------------------------------\n"
            + "------------------- Starting Backend ---------------------\n"
            + "----------------------------------------------------------\n"
        )
        self.update_console_text(msg)

        server.start_server(self.ctx, self._debug)

        # TODO: fix plugin monitor with new worker class
        # pluginMonitor.start_monitor()
        # for ii, proc in enumerate(pluginMonitor.running_procs):
        #     proc.readyReadStandardOutput.connect(partial(self._print_plug_msg, ii))

        # starting a thread to run the conn_server
        worker = Worker(
            conn_server.ConnServer.start_conn_server,
            self.__process_events,
            self._debug,
            self.ctx,
        )
        # worker = Worker(conn_server.ConnServer.start_conn_server, self.ctx)
        self.threadpool.start(worker)

    @pyqtSlot()
    def clicked_stop(self):
        """Actions to perform when the stop button is clicked."""
        succ = self._stop_subtasks()

        if succ:
            msg = (
                "----------------------------------------------------------\n"
                + "------------------- Stopping Backend ---------------------\n"
                + "----------------------------------------------------------\n\n"
            )
            self.update_console_text(msg)

    @pyqtSlot(str)
    def changed_ip(self, text):
        """Called when the ip textbox is updated."""
        settings.IP = text

    @pyqtSlot(str)
    def changed_port(self, text):
        """Called when the port textbox is updated."""
        settings.PORT = int(text)

    def closeEvent(self, event):
        """Called when the window is closed."""
        # nicely close all
        self._stop_subtasks()

        sys.stdout.flush()
        sys.stderr.flush()
