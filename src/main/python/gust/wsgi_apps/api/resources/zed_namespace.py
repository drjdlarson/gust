"""Url definitions for the ZED interface."""
import logging
from flask import request
from flask_restx import Resource, Namespace

import gust.database as database
import gust.conn_manager.conn_settings as conn_settings
from gust.conn_manager import send_info_to_conn_server
from gust.wsgi_apps.api.url_bases import ZED
from zed import ConfigSet, write_config_file


logger = logging.getLogger("[URL-Manager]")

ZED_NS = Namespace(ZED)

con_parse = ZED_NS.parser()
con_parse.add_argument('id', default=-1, type=int)
con_parse.add_argument("name", default="", type=str)
con_parse.add_argument("hacDist", default=0.2, type=float)
con_parse.add_argument("updateHz", default=1, type=float)


@ZED_NS.route("/connect")
class ConnInfo(Resource):
    @ZED_NS.expect(con_parse)
    def get(self):
        cf = ConfigSet()
        args = con_parse.parse_args()
        cf.id = args["id"]
        cf.name = args["name"]
        hac_dist = args["hacDist"]
        update_hz = args["updateHz"]

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
            write_config_file(file_name, [cf,])
            res = database.add_zed(cf.name, file_name)
            if res:
                msg = {
                    "name": cf.name,
                    "config": file_name,
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
