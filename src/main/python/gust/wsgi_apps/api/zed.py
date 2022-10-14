"""Url definitions for the ZED interface."""
import logging
from flask import request
from flask_restx import Resource

import gust.database as database
import gust.conn_manager.conn_settings as conn_settings
from gust.wsgi_apps.api.app import api
from gust.conn_manager import send_info_to_conn_server
from gust.wsgi_apps.api.url_bases import ZED
from zed import ConfigSet, write_config_file


logger = logging.getLogger("[URL-Manager]")


@api.route("{:s}/connect".format(ZED))
class ConnInfo(Resource):
    def get(self):
        cf = ConfigSet()
        cf.id = request.args.get("id", default=-1, type=int)
        cf.name = request.args.get("name", default="", type=str)
        hac_dist = request.args.get("hacDist", default=0.2, type=float)
        update_hz = request.args.get("updateHz", default=1, type=float)

        # loc_x = request.args.get("locx", default=0, type=float)
        # loc_y = request.args.get("locy", default=0, type=float)
        # loc_z = request.args.get("locz", default=0, type=float)
        # dcm00 = request.args.get("dcm00", default=1, type=float)
        # dcm11 = request.args.get("dcm11", default=1, type=float)
        # dcm22 = request.args.get("dcm22", default=1, type=float)
        # dcm01 = request.args.get("dcm01", default=0, type=float)
        # dcm02 = request.args.get("dcm02", default=0, type=float)
        # dcm03 = request.args.get("dcm03", default=0, type=float)

        if cf.valid:
            database.connect_db()
            file_name = "zed_{:d}.yaml".format(cf.id)
            config_file = write_config_file(file_name, [cf,])
            res = database.add_zed(cf.name, config_file)
            if res:
                msg = {
                    "name": cf.name,
                    "config": config_file,
                    "hac_dist": hac_dist,
                    "update_rate": 1.0 / update_hz,
                }
                conn_succ, info = send_info_to_conn_server(msg, conn_settings.ZED_CONN)
                if conn_succ:
                    return {"success": True, "msg": ""}
                else:
                    return {"success": False, "msg": "Error connecting"}
            else:
                return {"success": False, "msg": "Unable to add zed to database"}
        else:
            return {"success": False, "msg": "Invalid zed config"}
