"""Handle all plugin related operations."""
import os
import sys
import logging
import platform
import json

from PyQt5.QtCore import QProcess, QObject, pyqtSlot
from PyQt5 import QtNetwork


class PluginMonitor(QObject):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(PluginMonitor, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()

        self.plugin_dir = ''
        self.avail_plugins = []

        self.port = 9500
        self.host = '127.0.0.1'

        self.udp_sock = QtNetwork.QUdpSocket()

        self.running_procs = []
        self.running_names = []
        self.running_ids = []

        if 'windows' in platform.system().lower():
            self.file_ext = '.exe'
        else:
            self.file_ext = ''

    def get_plugin_exe(self, plugin_name):
        return os.path.join(self.plugin_dir, plugin_name,
                            '{}{}'.format(plugin_name, self.file_ext))

    def validate_plugins(self, folders):
        plugins = []
        for f in folders:
            if os.path.exists(self.get_plugin_exe(f)):
                plugins.append(f)
        return plugins

    def scan_for_plugins(self):
        logging.info('[plugin-monitor] Scanning for plugins')

        folders = next(os.walk(self.plugin_dir))[1]

        plugins = self.validate_plugins(folders)
        self.avail_plugins = plugins

        # TODO: is there a fail condition here?
        return True

    def _proc_pending_data(self):
        import gust.database as database

        while self.udp_sock.hasPendingDatagrams():
            datagram = self.udp_sock.receiveDatagram(self.udp_sock.pendingDatagramSize())
            packet = json.loads(datagram.data().data())
            p_name = packet['plugin_name']
            p_id = packet['id']
            data = packet['data']

            # add data to database
            if not database.add_plugin_data(p_name, p_id, data):
                msg = 'Failed to log data for plugin: {} with ID: {}'
                logging.critical(msg.format(p_name, p_id))

    def _start_server(self):
        if self.udp_sock.state() == QtNetwork.QAbstractSocket.SocketState.UnconnectedState:
            self.udp_sock.bind(self.port)
            self.udp_sock.readyRead.connect(self._proc_pending_data)

        return self.udp_sock.state() == QtNetwork.QAbstractSocket.SocketState.ConnectedState

    def _start_plugins(self):
        import gust.database as database

        # get data from database
        des_plugins = database.get_plugin_names(True)

        for p_name in des_plugins:
            plugin_ids = None
            for p_id in plugin_ids:
                logging.info('[plugin-monitor] Starting plugin: {:s} ID: {:d}'.format(p_name, p_id))

                proc = QProcess()
                proc.setProcessChannelMode(QProcess.MergedChannels)

                program = self.get_plugin_exe(p_name)
                args = ['-p {:d}'.format(self.port),
                        '{:d}'.format(p_id)]
                proc.start(program, args)

                self.running_procs.append(proc)
                self.running_names.append(p_name)
                self.running_ids.append(p_id)

        return True

    @pyqtSlot()
    def start_monitor(self):
        logging.info('[plugin-monitor] Starting monitor')
        if not self._start_server():
            pass
            # raise RuntimeError()

        if not self._start_plugins:
            raise RuntimeError()

        return True

    def stop_monitor(self):
        for proc in self.running_procs:
            proc.terminate()

        self.running_procs = []

        return True

    def extract_schema_fields(self, p_name):
        pass


pluginMonitor = PluginMonitor()
