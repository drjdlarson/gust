"""Handle all plugin related operations."""
import os
import sys
import logging
import platform
import json

from PyQt5.QtCore import QProcess, QObject, pyqtSlot
from PyQt5 import QtNetwork

logger = logging.getLogger('[plugin-monitor]')


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
        logger.info('Scanning for plugins')

        folders = next(os.walk(self.plugin_dir))[1]

        plugins = self.validate_plugins(folders)
        self.avail_plugins = plugins

        # TODO: is there a fail condition here?
        return True

    def _proc_pending_data(self):
        import utilities.database as database

        while self.udp_sock.hasPendingDatagrams():
            datagram = self.udp_sock.receiveDatagram(self.udp_sock.pendingDatagramSize())
            packet = json.loads(datagram.data().data())
            p_name = packet['plugin_name']
            p_id = packet['id']
            data = packet['data']

            logger.info('Rec from Plugin: {:s} ID: {:d} Data: {:}'.format(p_name, p_id, data))

            # add data to database
            schema = self.extract_schema_data_fields(p_name)
            if not database.add_plugin_data(p_name, p_id, data, schema):
                msg = 'Failed to log data for plugin: {} with ID: {}'
                logger.critical(msg.format(p_name, p_id))

    def _start_server(self):
        # if self.udp_sock.state() == QtNetwork.QAbstractSocket.SocketState.UnconnectedState:
        self.udp_sock.bind(self.port)
        self.udp_sock.readyRead.connect(self._proc_pending_data)

        return True
        # return self.udp_sock.state() == QtNetwork.QAbstractSocket.SocketState.ConnectedState


    def _start_plugins(self):
        import utilities.database as database

        # get data from database
        des_plugins = database.get_plugin_names(True)
        logger.info('found desired plugins: {}'.format(des_plugins))

        for p_name in des_plugins:
            plugin_ids = database.get_plugin_ids(p_name)
            cwd = os.path.join(self.plugin_dir, p_name)
            for p_id in plugin_ids:
                logger.info('Starting plugin: {:s} ID: {:d}'.format(p_name, p_id))
                logger.debug('Working directory is {:s}'.format(cwd))

                proc = QProcess()
                proc.setProcessChannelMode(QProcess.MergedChannels)
                proc.setWorkingDirectory(cwd)

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
        logger.info('Starting monitor')
        if not self._start_server():
            raise RuntimeError()

        if not self._start_plugins():
            raise RuntimeError()

        return True

    def stop_monitor(self):
        for proc in self.running_procs:
            proc.terminate()

        self.running_procs = []
        self.running_names = []
        self.running_ids = []

        return True

    def extract_schema_data_fields(self, p_name):
        schema = self.load_schema_file(p_name)

        fields = []
        for key, val in schema['data'].items():
            if type(val).__name__ == 'dict':
                msg = 'Dictionaries are not supported. Found in plugin {:s}'
                logger.critical(msg.format(p_name))
                continue
            fields.append((key, val))

        return fields

    def load_schema_file(self, p_name):
        fpath = self.find_schema_file(p_name)
        with open(fpath, 'r') as fin:
            schema = json.load(fin)

        return schema

    def find_schema_file(self, p_name):
        fpath = os.path.join(self.plugin_dir, p_name, '{:s}_schema.json'.format(p_name))
        if not os.path.exists(fpath):
            logger.critical('Failed to find schema file {:s}'.format(fpath))
            return None
        return fpath


pluginMonitor = PluginMonitor()
