import os
from PyQt5.QtCore import QProcess, pyqtSlot
from PyQt5 import QtNetwork

import gust.database as database

class PluginMonitor:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
          cls.instance = super(PluginMonitor, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.plugin_dir = ''
        self.avail_plugins = []
        self.des_plugins = []
        self.db_cons = {}

        self.port = 9500
        self.host = '127.0.0.1'

        self.udp_sock = QtNetwork.QUdpSocket()

        # self.proc = QProcess()
        # self.proc.setProcessChannelMode(QProcess.MergedChannels)

    def scan_for_plugins(self):
        folders = next(os.walk(self.plugin_dir))[1]

        # TODO: eventually do some checking here to make sure plugins are valid
        self.avail_plugins = folders

        # TODO: is there a fail condition here?
        return True

    def _proc_pending_data(self):
        while self.udp_sock.hasPendingDatagrams():
            packet, host, port = self.udp_sock.readDatagram(self.udp_sock.pendingDatagramSize())
            # determine database connection (plug name + id)
            # add data to database

    def _start_server(self):
        self.udp_sock.bind(self.port)
        self.udp_sock.readyRead.connect(self._proc_pending_data)

        # self.proc.start('python', ['gust.plugins', '{:d}'.format(self.port)])

        return True

    def _start_plugins(self):
        for plugin in self.des_plugins:
            proc = QProcess()
            proc.setProcessChannelMode(QProcess.MergedChannels)

            for plug_id in range(100):
                key = '{:s}{:02d}'.format(plugin.name, plug_id)
                if key not in self.db_cons:
                    break

            program = plugin.name
            args = ['-p {:d} {:d}'.format(self.port, plug_id)]
            proc.start(program, args)

            con = database.connect_to_database(con_name=key)
            self.db_cons[key] = (con, proc)

        return True

    def start_monitor(self):
        if not self._start_server():
            raise RuntimeError()

        if not self._start_plugins:
            raise RuntimeError()

        return True

    def stop_monitor(self):
        # does anything need to happen here?
        return True

pluginMonitor = PluginMonitor()


# --------------------
# in GUST:
    # start plugin monitor subprocess:
        # scan plugins directory for new folders (plugins) of compiled python
        # keep list of what plugins are available
        # start local server to listen for plugin connections
        # start each desired plugin and create database connection for it
        # main loop:
            # listen for new UDP packets with data
            # write data to appropriate database table

# in plugin:
    # handle any custom library imports for sensor
    # handle reading from proper hardware
    # format data into UDP packet of appropriate format
    # send UDP packet to plugin monitor's port on localhost (port is config)
        # must contain plugin name and id (require id from cmd line)

# in gust-plugin-tool:
    # provide function for sending data to server in expected format
    # provide __name__ == __main__ entry point with argument parser for port
    # provide method for creating executable (e.g. PyInstaller, cx_freeze)
    # provide method for testing generated executable (listen for data and print to console)
