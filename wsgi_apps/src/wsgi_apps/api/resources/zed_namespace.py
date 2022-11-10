"""Url definitions for the ZED interface."""
import logging
import numpy as np
from flask_restx import Resource, Namespace

import utilities.database as database
from utilities import ConnSettings as conn_settings
from utilities import send_info_to_conn_server
from wsgi_apps.api.url_bases import ZED
from zed import ConfigSet, write_config_file


logger = logging.getLogger("[URL-Manager]")

ZED_NS = Namespace(ZED)

conParse = ZED_NS.parser()
conParse.add_argument('id', default=-1, type=int)
conParse.add_argument("name", default="", type=str)
conParse.add_argument("locx", default=0, type=float)
conParse.add_argument("locy", default=0, type=float)
conParse.add_argument("locz", default=0, type=float)
conParse.add_argument("dcm00", default=1, type=float)
conParse.add_argument("dcm11", default=1, type=float)
conParse.add_argument("dcm22", default=1, type=float)
conParse.add_argument("dcm01", default=0, type=float)
conParse.add_argument("dcm02", default=0, type=float)
conParse.add_argument("dcm10", default=0, type=float)
conParse.add_argument("dcm12", default=0, type=float)
conParse.add_argument("dcm20", default=0, type=float)
conParse.add_argument("dcm21", default=0, type=float)
conParse.add_argument("req_cal", default=False, type=float)
conParse.add_argument("minx", default=0, type=float)
conParse.add_argument("miny", default=0, type=float)
conParse.add_argument("minz", default=0, type=float)
conParse.add_argument("maxx", default=0, type=float)
conParse.add_argument("maxy", default=0, type=float)
conParse.add_argument("maxz", default=0, type=float)
conParse.add_argument("conf", default=60, type=int)
conParse.add_argument("tex_conf", default=40, type=int)
conParse.add_argument("hacDist", default=0.2, type=float)
conParse.add_argument("updateHz", default=1, type=float)


@ZED_NS.route("/connect")
class ConnInfo(Resource):
    @ZED_NS.expect(conParse)
    def get(self):
        cf = ConfigSet()
        args = conParse.parse_args()
        cf.id = args["id"]
        cf.name = args["name"]
        cf.loc = np.array([args["locx"], args["locy"], args["locz"]])
        cf.dcm = np.array([[args["dcm00"], args["dcm01"], args["dcm02"]],
                           [args["dcm10"], args["dcm11"], args["dcm12"]],
                           [args["dcm20"], args["dcm21"], args["dcm22"]]])
        cf.req_cal = args["req_cal"]
        cf.min = np.array([args["minx"], args["miny"], args["minz"]])
        cf.max= np.array([args["maxx"], args["maxy"], args["maxz"]])
        cf.conf = args["conf"]
        cf.tex_conf = args["tex_conf"]
        hac_dist = args["hacDist"]
        update_hz = args["updateHz"]

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



getCurPointsParse = ZED_NS.parser()
getCurPointsParse.add_argument('name', type=str, default='')

@ZED_NS.route("/get_current_points")
class GetCurPoints(Resource):
    @ZED_NS.expect(getCurPointsParse)
    def get(self):
        args = getCurPointsParse.parse_args()
        database.connect_db()

        return database.get_zed_points(args.name)
