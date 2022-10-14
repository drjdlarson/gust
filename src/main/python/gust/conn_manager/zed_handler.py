import time
import logging
from PyQt5.QtCore import QThreadPool, QTimer, pyqtSlot, pyqtSignal, QObject

import gust.database as database
from gust.worker import Worker
from zed import zedManager


logger = logging.getLogger("[zed-manager]")


class ZedHandler(QObject):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.running = {}
        self.update_rates = {}
        self.hac_dist = {}
        self.debug = False

    def connect(self, info):
        name = info["name"]

        if zedManager.connect_to_cameras(filename=info["config"]):
            self.hac_dist[name] = info["hac_dist"]
            self.update_rates[name] = info["update_rate"]
            self.running[name] = True

            worker = Worker(self.poll, name)
            self.threadpool.start(worker)

            return {"success": True, "info": ""}
        else:
            return {"success": False, "info": "Failed to connect to zed"}

    def poll(self, name):
        cam = zedManager.cameras[0]
        while self.running[name]:
            meas_arr = cam.extract_objects(max_dist=self.hac_dist[name])
            posix = time.time()
            for m in meas_arr:
                database.write_zed_obj(name, posix, m)
            time.sleep(self.update_rates[name])

    @classmethod
    def kill(cls):
        zedManager.shutdown()


zedHandler = ZedHandler()
