"""Handle database operations."""
import os
import logging
import enum
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

#################
# DO NOT CHANGE STRINGS IN THIS FILE (unless you are absolutely certain).
#################


# DB_FILE = 'test_database.sqlite'
DB_FILE_KEY = "GUST_DB_FILE"
DB_PATH_KEY = "GUST_DB_PATH"  # autoset by backend window on startup
DB_DRIVER = "QSQLITE"

_DB = None
_connected_counter = 0
_initialized_logger = False

logger = logging.getLogger(__name__)


def set_db_file(f):
    os.environ[DB_FILE_KEY] = f


def DB_FILE():
    """Returns the file name as saved in Resources"""
    return os.environ.get(DB_FILE_KEY, "gust_database.sqlite")


def set_db_path(p):
    os.environ[DB_PATH_KEY] = p


def DB_PATH():
    """Returns the file path of resources folder.
    This is set by BackendWindow.setup()"""
    return os.environ.get(DB_PATH_KEY, "./")


@enum.unique
class DroneRates(enum.Enum):
    """Enums to define different sets of telemetry data."""

    RATE1 = enum.auto()
    RATE2 = enum.auto()
    RATE3 = enum.auto()
    RATE4 = enum.auto()

    def __str__(self):
        return self.name.lower()


def db_name():
    """Full path of database file.

    Returns
    -------
    str
        full path of the database file.
    """
    return os.path.join(DB_PATH(), DB_FILE())


def setup_logger():
    """Handles setting up the logger stuff."""

    global _initialized_logger

    if not _initialized_logger:
        ch = logging.StreamHandler()

        # if args.debug:
        #     logger.setLevel(logging.DEBUG)
        #     ch.setLevel(logging.DEBUG)
        # else:
        logger.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[database] %(levelname)s %(asctime)s - %(message)s"
        )
        ch.setFormatter(formatter)

        logger.addHandler(ch)

        _initialized_logger = True


def open_db(location_file):
    """
    Opens the database. This is first called by BackendWindow.setup(). Database
    needs to be open before any other operation with GUST.

    Parameters
    ----------
    location_file: str
        File path of saved locations file stored in Resources.

    Returns
    -------

    """
    global _DB
    # Don't do anything if the database is already open.
    if _DB is not None:
        logger.critical("Database has already been opened it is: {}".format(repr(_DB)))
        return

    setup_logger()

    # create a new database
    _DB = QSqlDatabase.addDatabase(DB_DRIVER)
    fpath = db_name()
    logger.info("logger: {}".format(fpath))

    # delete the file if it already exists.
    if os.path.exists(fpath):
        logger.info("Removing existing database {}".format(fpath))
        os.remove(fpath)

    _DB.setDatabaseName(fpath)

    # The database should be open at this point.
    if not _DB.open():
        logger.critical("Unable to open database")

    # Creating a table for plugins collection.
    query = _start_query()
    cmd = """CREATE TABLE IF NOT EXISTS PluginCollection (
        collection_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name VARCHAR(32) );"""
    logger.debug(cmd)
    res1 = query.exec_(cmd)
    if not res1:
        logger.critical(query.lastError().text())

    # Creating a table for drone collection. Vehicles information is saved with a
    # unique id and name
    query = _start_query()
    cmd = """CREATE TABLE IF NOT EXISTS drone_collection (
    uid INTEGER PRIMARY KEY,
    name TEXT,
    port TEXT,
    color TEXT,
    connection INT,
    UNIQUE(uid, name)
    );
    """
    logger.debug(cmd)
    res2 = query.exec_(cmd)
    if not res2:
        logger.critical(query.lastError().text())

    # Creating a table for Zed connection information
    cmd = """CREATE TABLE IF NOT EXISTS zed_collection (
    uid INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT NOT NULL,
    config TEXT NOT NULL
    );
    """
    logger.debug(cmd)
    res3 = query.exec_(cmd)

    # Creating a table to store saved locations information.
    cmd = """CREATE TABLE IF NOT EXISTS locations (
        uid INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT NOT NULL,
        coords TEXT NOT NULL
        );
        """
    logger.debug(cmd)
    res4 = query.exec_(cmd)

    if res4:
        res4 = write_saved_locations_in_db(location_file)

    if res1 and res2 and res3 and res4:
        logger.info("Database is now open")


def write_saved_locations_in_db(location_fpath):
    """Store saved locations info in the database."""
    query = _start_query()
    results = []
    with open(location_fpath, "r") as fin:
        for ii, line in enumerate(fin):
            if ii == 0:
                continue
            tokens = line.strip().split("=")
            if len(tokens) != 2:
                continue
            name = tokens[0]

            if "#" in tokens[1]:
                ind = tokens[1].find("#")
                coords = tokens[1][:ind]
            else:
                coords = tokens[1]
            cmd = "INSERT into locations (name, coords) VALUES ('{}', '{}');".format(
                name, coords
            )
            logger.debug(cmd)
            res = query.exec_(cmd)
            results.append(res)
    # Returns True only if all queries are successful.
    return all(results)


def connect_db():
    """Connect to the database. This is required before interacting with the database."""

    global _DB
    setup_logger()

    # Don't do anything if the database is already open
    if _DB is not None:
        # logger.info("Database is already open")
        return True

    # create database
    _DB = QSqlDatabase.addDatabase(DB_DRIVER)
    fpath = db_name()

    if not os.path.exists(fpath):
        logger.warning("Database file doesn't exist")
        return False

    _DB.setDatabaseName(fpath)

    if not _DB.open():
        logger.critical("Unable to open database")
        return False
    return True


def close_db():
    """Close the database."""
    global _DB
    _DB.close()


def _start_query():
    """Starts a QSqlQuery. The query object to used to send commands to the database."""
    global _DB
    query = QSqlQuery(_DB)
    query.exec_("PRAGMA foreign_keys=ON;")
    return query


def _create_new_ids_table(p_name):
    query = _start_query()

    # create new table, not always required
    cmd = (
        "CREATE TABLE {:s}_ids ( id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE );".format(
            p_name
        )
    )
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    # create temp table for copying PluginCollection, not always required
    rec = _DB.record("PluginCollection")
    col_names = [rec.fieldName(ii) for ii in range(rec.count())]
    fmt = """CREATE TABLE _tmp (
        collection_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name VARCHAR(32)"""
    existing_fks = []
    for col in col_names:
        if col in ("collection_id", "name"):
            continue
        fmt += ",\n{:8s}{:s} INTEGER UNIQUE DEFAULT NULL".format("", col)
        existing_fks.append(col)

    new_fk = "{:s}_id".format(p_name)
    fmt += ",\n{:8s}{:s} INTEGER UNIQUE DEFAULT NULL".format("", new_fk)
    combined_fks = existing_fks + [
        new_fk,
    ]

    fk_fmt = ""
    for ii, col in enumerate(combined_fks):
        fk_fmt += ",\n{:8s}FOREIGN KEY ({:s}) REFERENCES {:s}s(id) ON UPDATE CASCADE ON DELETE CASCADE".format(
            "", col, col
        )

    cmd = "{:s}{:s});".format(fmt, fk_fmt)
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    # copy PluginCollection to temp table, not always required
    if len(existing_fks) > 0:
        joined = ", ".join(existing_fks)
        cmd = "INSERT INTO _tmp(name, {:s}) SELECT name, {:s} FROM PluginCollection;".format(
            joined, joined
        )
    else:
        cmd = "INSERT INTO _tmp(name) SELECT name FROM PluginCollection;"
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    # drop PluginCollection table, not always required
    cmd = "DROP TABLE PluginCollection;"
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    # rename temp table, not always required
    cmd = "ALTER TABLE _tmp RENAME to PluginCollection;"
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())


def _create_name_id_data_table(p_name, p_id, schema_fields):
    query = _start_query()

    base = """CREATE TABLE {:s}_{:d}_data (
        time_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        p_id INTEGER""".format(
        p_name, p_id
    )
    tail = """,
        FOREIGN KEY (p_id) REFERENCES {:s}_ids(id) ON UPDATE CASCADE ON DELETE CASCADE );""".format(
        p_name
    )

    mid = ""
    for key, val in schema_fields:
        if val.lower() == "int":
            dtype = "INTEGER"
        elif val.lower() in ("float", "double"):
            dtype = "REAL"
        elif val.lower() == "str":
            dtype = "TEXT"
        else:
            msg = "Database does not support data type {} from schema for plugin {}"
            logger.critical(msg.format(val, p_name))
            continue

        mid += ",\n{:8s}{:s} {:s}".format("", key, dtype)

    cmd = "{:s}{:s}{:s}".format(base, mid, tail)

    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())


def _add_new_id_val(p_name):
    query = _start_query()

    cmd = "INSERT INTO {:s}_ids (id) VALUES (NULL);".format(p_name)
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    cmd = "SELECT LAST_VALUE(id) OVER (ORDER BY id DESC) FROM {:s}_ids".format(p_name)
    logger.debug(cmd)
    query.exec_(cmd)

    query.first()
    return int(query.value(0))


def _add_new_pc_val(p_name, p_id):
    query = _start_query()

    cmd = "INSERT INTO PluginCollection (name, {:s}_id) VALUES ('{:s}', {:d});".format(
        p_name, p_name, p_id
    )
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())


def add_plugin(p_name):
    """Add a new plugin to the database, account for multiple of the same name.

    Parameters
    ----------
    p_name : string
        Name of the plugin.

    Returns
    -------
    p_id : int
        ID of the plugin that was added.
    """
    from gust.plugin_monitor import pluginMonitor

    global _DB

    if "{:s}_ids".format(p_name) not in _DB.tables():
        # create new name_ids table
        _create_new_ids_table(p_name)

        # add new val to name_id table
        p_id = _add_new_id_val(p_name)

        # add new val to pc table
        _add_new_pc_val(p_name, p_id)

        # create name_id_data
        if "{:s}_{:d}_data".format(p_name, p_id) not in _DB.tables():
            schema_fields = pluginMonitor.extract_schema_data_fields(p_name)
            _create_name_id_data_table(p_name, p_id, schema_fields)

    else:
        # add new val to name_id table
        p_id = _add_new_id_val(p_name)

        # add new val to pc table
        _add_new_pc_val(p_name, p_id)

        # create name_id_data
        if "{:s}_{:d}_data".format(p_name, p_id) not in _DB.tables():
            schema_fields = pluginMonitor.extract_schema_data_fields(p_name)
            _create_name_id_data_table(p_name, p_id, schema_fields)

    return p_id


def remove_plugin(p_name, p_id):
    if "{:s}_ids".format(p_name) in _DB.tables():
        query = _start_query()
        cmd = "DELETE FROM {:s}_ids WHERE id = {:d}".format(p_name, p_id)
        logger.debug(cmd)
        res = query.exec_(cmd)
        if not res:
            logger.critical(query.lastError().text())

        return res

    else:
        return False


def remove_plugin_by_col_id(col_ids):
    query = _start_query()
    for c_id in col_ids:
        cmd = "SELECT name FROM PluginCollection WHERE collection_id = {:d}".format(
            c_id
        )
        logger.debug(cmd)
        res = query.exec_(cmd)
        if not res:
            logger.critical(query.lastError().text())
            break
        query.first()
        p_name = query.value(0)

        cmd = "SELECT {:s}_id FROM PluginCollection WHERE collection_id = {:d}".format(
            p_name, c_id
        )
        logger.debug(cmd)
        res = query.exec_(cmd)
        if not res:
            logger.critical(query.lastError().text())
            break
        query.first()
        p_id = int(query.value(0))

        if not remove_plugin(p_name, p_id):
            logger.critical(
                "Failed to completely remove Plugin: {} ID: {}".format(p_name, p_id)
            )


def add_plugin_data(p_name, p_id, data, schema):
    tbl = "{:s}_{:d}_data".format(p_name, p_id)
    if tbl not in _DB.tables():
        return False

    query = _start_query()
    cmd = """INSERT INTO {:s} (
        p_id""".format(
        tbl
    )

    for key, val in schema:
        cmd += ",\n{:8s}{:s}".format("", key)

    cmd += """)\nVALUES (
        {:d}""".format(
        p_id
    )

    for key, dtype in schema:
        if key not in data:
            logger.critical(
                "Missing {:s} in packet from Plugin: {:s} ID: {:d}".format(
                    key, p_name, p_id
                )
            )
            return False

        if dtype == "str":
            cmd += ",\n{:8s}" "{}" "".format("", data[key])
        else:
            cmd += ",\n{:8s}{}".format("", data[key])

    cmd += ");"
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())
        return False

    return True


def get_plugin_names(distinct):
    if distinct:
        extra = "DISTINCT"
    else:
        extra = ""

    query = _start_query()
    cmd = "SELECT {:s} name FROM PluginCollection".format(extra)
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())
        return []

    query.seek(-1)
    plugin_names = []
    while query.next():
        plugin_names.append(query.value(0))

    return plugin_names


def get_plugin_ids(p_name):
    query = _start_query()

    tbl = "{:s}_ids".format(p_name)
    if tbl not in _DB.tables():
        logger.critical("Failed to find id table for plugin {:s}".format(p_name))
        return []

    cmd = "SELECT id FROM {:s}".format(tbl)
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())
        return []

    query.seek(-1)
    p_ids = []
    while query.next():
        p_ids.append(query.value(0))

    return p_ids


def get_drone_ids(distinct=True, active=True):
    """
    Shows all the drones currently in the database

    Parameters
    ----------
    distinct : bool, optional
        If True, it only returns unique drones.
    active : bool, optional
        If True, it only returns vehicles that are still connected
        connection value in drone_collection

    Returns
    -------
    list
        Names of vehicle in the database.

    """
    if distinct:
        extra1 = " DISTINCT"
    else:
        extra1 = ""

    # disconnected vehicles will have connection == 0, but they will still remain
    # in the database.
    if active:
        extra2 = "WHERE connection IS 1"
    else:
        extra2 = ""

    query = _start_query()
    if "drone_collection" not in _DB.tables():
        logger.critical("Unable to find drone_collection in database")

    cmd = "SELECT {} name FROM drone_collection {}".format(extra1, extra2)
    result = query.exec_(cmd)

    # query.seek(-1)
    names = []
    while result and query.next():
        names.append(query.value(0))
    return names


def create_zed_table_name(name):
    return "zed_data_{:s}".format(name.replace(" ", "_").lower())


def add_zed(name, config):
    """Add a new item in the zed_connection table"""
    query = _start_query()

    cmd = 'INSERT into zed_collection (name, config) VALUES ("{:s}", "{:s}");'.format(
        name, config
    )
    logger.info(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())
        return False

    cmd = """CREATE TABLE IF NOT EXISTS {:s} (
    posix INTEGER,
    xpos FLOAT,
    ypos FLOAT,
    zpos FLOAT
    );
    """.format(
        create_zed_table_name(name)
    )
    logger.info(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())
        return False
    return True


def add_vehicle(name, port, color):
    """
    Add a new vehicle in the database with all necessary tables.

    Parameters
    ----------
    name : str
        name of the vehicle
    port : str
        port used for vehicle connection
    color : str
        Color selected for the vehicle

    Returns
    -------

    """
    global _connected_counter
    query = _start_query()

    # adding vehicle's info to the main table
    cmd = 'INSERT into drone_collection (uid, name, port, color, connection) VALUES ({}, "{}", "{}", "{}", 1);'.format(
        _connected_counter, name, port, color
    )
    logger.info("Adding vehicle {} into drone collection".format(name))
    res1 = query.exec_(cmd)

    # adding the rate tables
    table_name = create_drone_rate_table_name(name, DroneRates.RATE1)
    cmd = """CREATE TABLE IF NOT EXISTS {:s} (
       	m_time float PRIMARY key,
    	home_lat float,
       	home_lon float,
       	home_alt float,
       	voltage float,
       	current float
     );""".format(
        table_name
    )
    res2 = query.exec_(cmd)

    table_name = create_drone_rate_table_name(name, DroneRates.RATE2)
    cmd = """CREATE TABLE IF NOT EXISTS {:s} (
       m_time float PRIMARY key,
       latitude float,
       longitude float,
       relative_alt float,
       yaw int,
       heading int,
       gnss_fix int,
       satellites_visible int,
       roll_angle float,
       pitch_angle float,
       alpha float,
       beta float,
       airspeed float,
       gndspeed float,
       vspeed float,
       throttle float
     );""".format(
        table_name
    )
    res3 = query.exec_(cmd)

    table_name = create_drone_rate_table_name(name, DroneRates.RATE3)
    cmd = """CREATE TABLE IF NOT EXISTS {:s} (
       m_time float PRIMARY key,
       chancount int,
       chan1_raw float,
       chan2_raw float,
       chan3_raw float,
       chan4_raw float,
       chan5_raw float,
       chan6_raw float,
       chan7_raw float,
       chan8_raw float,
       chan9_raw float,
       chan10_raw float,
       chan11_raw float,
       chan12_raw float,
       chan13_raw float,
       chan14_raw float,
       chan15_raw float,
       chan16_raw float,
       chan17_raw float,
       chan18_raw float,
       rssi float,
       servo_port text,
       servo1_raw float,
       servo2_raw float,
       servo3_raw float,
       servo4_raw float,
       servo5_raw float,
       servo6_raw float,
       servo7_raw float,
       servo8_raw float,
       servo9_raw float,
       servo10_raw float,
       servo11_raw float,
       servo12_raw float,
       servo13_raw float,
       servo14_raw float,
       servo15_raw float,
       servo16_raw float
     );""".format(
        table_name
    )
    res4 = query.exec_(cmd)

    table_name = create_drone_rate_table_name(name, DroneRates.RATE4)
    cmd = """CREATE TABLE IF NOT EXISTS {:s} (
       m_time float PRIMARY key,
       armed int,
       flight_mode Text,
       ekf_ok int,
       vehicle_type int,
       sys_status Text,
       tof int,
       next_wp int,
       relay_sw int,
       engine_sw int
     );""".format(
        table_name
    )
    res5 = query.exec_(cmd)

    table_name = name + "_mission"
    cmd = """CREATE TABLE IF NOT EXISTS {:s} (
    seq int,
    current int,
    frame int,
    command int,
    param1 float,
    param2 float,
    param3 float,
    param4 float,
    x float,
    y float,
    z float,
    autocontinue int
    );""".format(
        table_name
    )
    res6 = query.exec_(cmd)

    res = res1 and res2 and res3 and res4 and res5 and res6
    if res:
        _connected_counter += 1
    return res


def remove_vehicle(name):
    """Remove the vehicle from the database"""

    query = _start_query()

    cmd = "DELETE FROM drone_collection WHERE name LIKE '%{}%';".format(name)
    res = query.exec_(cmd)
    if res:
        logger.info("Deleted {} from drone_collection".format(name))
    else:
        logger.warning("Unable to delete {} from drone_collection".format(name))
        return

    rates = [member.name for member in DroneRates]
    rates = [x.lower() for x in rates]
    res = []

    # deleting all the tables related to the vehicle.
    for i, rate in enumerate(rates):
        drop_rate = "DROP TABLE IF EXISTS {}".format(
            create_drone_rate_table_name(name, rate)
        )
        res.append(query.exec_(drop_rate))

    if all(res):
        logger.info("Removed {} from the database".format(name))
        return True
    else:
        logger.warning("Unable to remove {} from the database".format(name))
        return False


def get_params(table_name, params):
    """
    Get parameters from the database

    Parameters
    ----------
    table_name : str
        Table name
    params : list
        list of params whose values are requested

    Returns
    -------
    val : dict
        Dict of requested parameters and their values {param: value}
    """
    query = _start_query()
    req_params = ", ".join(params)
    cmd = "SELECT {} FROM {}".format(req_params, table_name)
    val = {}
    query.exec_(cmd)
    query.last()
    for param in params:
        val[param] = query.value(param)
    return val


def get_mission_items(vehicle_name):
    """Get the saved mission items for the vehicle."""
    query = _start_query()
    table_name = vehicle_name + "_mission"
    cmd = "SELECT x, y, z FROM {}".format(table_name)
    coords = []
    result = query.exec_(cmd)
    while result and query.next():
        coords.append((query.value("x"), query.value("y"), query.value("z")))
    return coords


def remove_older_mission_items(vehicle_name):
    """Delete the saved mission items for the vehicle."""
    query = _start_query()
    table_name = vehicle_name + "_mission"
    cmd = "DELETE FROM {}".format(table_name)
    query.exec_(cmd)


def create_drone_rate_table_name(name, rate):
    """Returns a table name for given vehicle name and rate"""
    return "{:s}_{:s}".format(name, rate)


def change_connection_status_value(name, val):
    """
    Change the connection value of the vehicle. This is set to 0 when the vehicle
    disconnects.

    Parameters
    ----------
    name : str
        Name of the vehicle
    val : int
        Either 0 or 1

    Returns
    -------
    res : bool
        Result of query performed

    """

    query = _start_query()
    cmd = """
    UPDATE drone_collection
    SET connection = {} WHERE name IS '{}';
    """.format(
        val, name
    )
    res = query.exec_(cmd)
    logger.debug("Changing connection status of {} to {}".format(name, val))
    return res


def add_values(vals, table_name):
    """
    Adds new telemetry data to the database.

    Parameters
    ----------
    vals : dict
        Set of flight data to be written into the database.
    table_name : str
        Table name of where to store data
        eg. drone0_rate1

    Returns
    -------
    None.

    """

    keys = ", ".join(list(vals.keys()))
    values = str(list(vals.values()))[1:-1]
    query = _start_query()
    cmd = "INSERT INTO {} ({}) VALUES ({});".format(table_name, keys, values)
    res = query.exec_(cmd)

    msg = "adding data in {}. and result {}".format(table_name, res)
    # logger.debug(cmd)

    return res


def write_values(flt_data, name):
    """
    Gets all parameters for a single vehicle.
    Then, sends it to add_values() to write on the database

    Parameters
    ----------
    flt_data : list
        List of dictionaries rate1 and rate2 for a single vehicle.
    name : str
        Name of the vehicle.

    Returns
    -------
    None.

    """
    res = []
    for item in flt_data:
        rate = item["rate"]
        table_name = create_drone_rate_table_name(name, rate)
        succ = add_values(item["vals"], table_name)
        res.append(succ)

        msg = "Data being added in the table: ".format(table_name)
        # logger.debug(msg)

    return all(res)


def get_drone_name(uid):
    """Gives the vehicle name for corresponding uid. uid indexing starts from 0"""
    query = _start_query()
    cmd = "SELECT name FROM drone_collection WHERE uid = {};".format(uid)
    query.exec_(cmd)
    query.last()
    return query.value(0)


def get_drone_color(name):
    """Returns the color associated with the drone"""
    query = _start_query()
    cmd = "SELECT color FROM drone_collection WHERE name IS '{}';".format(name)
    query.exec_(cmd)
    query.last()
    return query.value(0)


def get_used_colors():
    """Returns a list of colors being used by active drones"""
    query = _start_query()
    cmd = "SELECT color FROM drone_collection WHERE connection IS 1;"
    result = query.exec_(cmd)
    # query.seek(-1)
    colors = []
    while result and query.next():
        colors.append(query.value(0))
    return colors


def write_zed_obj(name, posix, obj):
    tab_name = create_zed_table_name(name)
    cmd = "INSERT INTO {:s} (posix, xpos, ypos, zpos) VALUES ({:f}, {:f}, {:f}, {:f});".format(
        tab_name, posix, obj[0], obj[1], obj[2]
    )
    query = _start_query()
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())
    return res


def write_zed_objs(name, posix, obj_lst):
    logger.debug("Writing zed objects to database")

    tab_name = create_zed_table_name(name)
    cmd = "INSERT INTO {:s} (posix, xpos, ypos, zpos) VALUES".format(tab_name)
    for ii, obj in enumerate(obj_lst):
        if ii > 0:
            cmd += ","
        cmd += "\n\t({:f}, {:f}, {:f}, {:f})".format(posix, obj[0], obj[1], obj[2])
    cmd += ";"

    query = _start_query()
    res = query.exec_(cmd)
    logger.debug(cmd)
    if not res:
        logger.critical(query.lastError().text())
    return res


def get_zed_points(name, delay=None):
    if delay is None:
        delay = 0

    ret_vals = {"xpos": [], "ypos": [], "zpos": []}

    if name is None or len(name) == 0:
        query = _start_query()
        cmd = "SELECT name FROM zed_collection"
        res = query.exec_(cmd)
        if not res:
            logger.critical(query.lastError().text())
            return ret_vals

        query.seek(-1)
        name_lst = []
        while query.next():
            name_lst.append(query.value(0))

        for n in name_lst:
            query = _start_query()
            tab_name = create_zed_table_name(n)
            cmd = "SELECT posix FROM {} ORDER BY rowid DESC LIMIT 1;".format(tab_name)
            res = query.exec_(cmd)
            if not res:
                logger.critical(query.lastError().text())
                return ret_vals

            query.last()
            if query.value(0) is None:
                continue

            cmd = "SELECT {}, {}, {} FROM {} WHERE posix >= {:.2f}".format(
                *list(ret_vals.keys()), tab_name, query.value(0) - 0.01 - delay
            )
            sub_q = _start_query()
            res = sub_q.exec_(cmd)
            if not res:
                logger.critical(sub_q.lastError().text())
                return ret_vals
            sub_q.seek(-1)
            while sub_q.next():
                for ii, param in enumerate(ret_vals.keys()):
                    ret_vals[param].append(sub_q.value(ii))

    else:
        tab_name = create_zed_table_name(name)
        query = _start_query()
        cmd = "SELECT posix FROM {} ORDER BY rowid DESC LIMIT 1;".format(tab_name)
        res = query.exec_(cmd)
        if not res:
            logger.critical(query.lastError().text())
            return ret_vals

        query.last()
        cmd = "SELECT {}, {}, {} FROM {} WHERE posix >= {:.2f}".format(
            *list(ret_vals.keys()), tab_name, query.value(0) - 0.01 - delay
        )
        logger.info(cmd)
        res = query.exec_(cmd)
        if not res:
            logger.critical(query.lastError().text())
            return ret_vals
        query.last()
        for ii, param in enumerate(["xpos", "ypos", "zpos"]):
            ret_vals[param] = query.value(param)

    return ret_vals


def add_cmr_table():
    """Adds a new table to handle CMR operation"""
    query = _start_query()
    cmd = """CREATE TABLE IF NOT EXISTS cmr_table (
    name TEXT,
    wp_color TEXT,
    next_wp INTEGER,
    wp_reached INTEGER,
    UNIQUE(name, wp_color)
    );
    """
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.warning("Unable to add CMR table")
    return res


def add_cmr_vehicle(name, wp_color):
    """Adds a new vehicle involved in CMR operation"""
    query = _start_query()
    cmd = """INSERT INTO cmr_table (name, wp_color, next_wp,wp_reached) VALUES ("{}", "{}", 1, 0);
    """.format(
        name, wp_color
    )
    res = query.exec_(cmd)
    if not res:
        logger.warning(
            "Unable to add {} with {} waypoints to cmr_table".format(name, wp_color)
        )
    return res


def get_saved_locations():
    """Returns a dict with information about saved locations."""
    query = _start_query()
    cmd = "SELECT name, coords FROM locations"
    val = {}
    result = query.exec_(cmd)
    while result and query.next():
        val[query.value("name")] = query.value("coords")
    return val


if __name__ == "__main__":
    import random
    import time

    open_db()
    print(add_vehicle("Testing", "/dev/test/"))
    res = add_vehicle("Testing2", "/dev/test/")
    add_vehicle("Tasting3", "/dev/test/")
    print(get_drone_ids(True, False))
    print(remove_vehicle("Tasting3"))
    print(get_drone_ids(True, False))

    # rates = [member.name for member in DroneRates]
    # rates = [x.lower() for x in rates]
    # print(rates)

    # rates = [member.name for member in DroneRates]
    # rates = [x.lower() for x in rates]
    # res = []
    # for i, rate in enumerate(rates):
    #     print(i)
    #     print(rate)
