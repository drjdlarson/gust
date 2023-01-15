import time
import logging
import utilities.database as database

from zed import zedManager
from zed import logger as zlogger


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ZedHandler():
    def __init__(self, debug=False):
        super().__init__()
        self.update_rates = {}
        self.hac_dist = {}

        ch = logging.StreamHandler()

        if debug:
            zlogger.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
        else:
            zlogger.setLevel(logging.INFO)
            ch.setLevel(logging.INFO)

        formatter = logging.Formatter('[zed-manager] %(levelname)s %(asctime)s - %(message)s')
        ch.setFormatter(formatter)

        zlogger.addHandler(ch)

    def connect(self, info):
        name = info["name"]
        logger.info(info)

        if zedManager.connect_to_cameras(filename=info["filename"]):
            self.hac_dist[name] = info["hac_dist"]
            self.update_rates[name] = info["update_rate"]


            return {"success": True, "info": ""}
        else:
            return {"success": False, "info": "Failed to connect to zed"}

    def poll(self, name):
        if not database.connect_db():
            self.kill()
            return

        cam = zedManager.cameras[0]
        while True:
            try:
                meas_arr = cam.extract_objects(max_dist=self.hac_dist[name])
                posix = time.time()
                for m in meas_arr:
                    database.write_zed_obj(name, posix, m)
            except TypeError:
                continue
            time.sleep(self.update_rates[name])

    def kill(self):
        zedManager.shutdown()


zedHandler = ZedHandler()