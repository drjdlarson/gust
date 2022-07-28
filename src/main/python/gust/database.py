"""Handle database operations."""
import os
import logging
from time import sleep
import enum
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


import serial.tools.list_ports

# DB_FILE = 'test_database.sqlite'
DB_FILE = 'dummy.sqlite'
DB_PATH = '/home/lagerprocessor/Projects/gust/src/main/resources/base/'
# DB_PATH = './'
DB_DRIVER = "QSQLITE"

_DB = None
_main_table = "drone_collection"

logger = logging.getLogger('[database]')

# TODO: make this thread safe, figure out open_db()


@enum.unique
class DroneRates(enum.Enum):

    RATE1 = enum.auto()
    RATE2 = enum.auto()

    def __str__(self):
        return self.name.lower()


def db_name():
    """Full path of database file.

    Returns
    -------
    str
        full path of the database file.
    """
    global DB_PATH, DB_FILE
    return os.path.join(DB_PATH, DB_FILE)


def open_db():
    """Open the database by removing the old file and creating a new one.

    This must be called once before any database operations occur.

    Returns
    -------
    None.
    """
    global _DB

    if _DB is not None:
        return
    # create database
    _DB = QSqlDatabase.addDatabase(DB_DRIVER)
    fpath = db_name()

    if os.path.exists(fpath):
        logger.debug('Removing existing database {}'.format(fpath))
        os.remove(fpath)

    _DB.setDatabaseName(fpath)
    _DB.open()

    if not _DB.open():
        logger.critical("Unable to open database")

    query = _start_query()
    cmd = '''CREATE TABLE IF NOT EXISTS PluginCollection (
        collection_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name VARCHAR(32) );'''
    logger.debug(cmd)
    res1 = query.exec_(cmd)
    if not res1:
        logger.critical(query.lastError().text())

    query = _start_query()
    cmd = """CREATE TABLE IF NOT EXISTS drone_collection (
    uid INTEGER PRIMARY KEY,
    name TEXT,
    port TEXT,
    UNIQUE(uid, name, port)
    );
    """
    logger.debug(cmd)
    res2 = query.exec_(cmd)
    if not res2:
        logger.critical(query.lastError().text())

    if res1 and res2:
        logger.info("Database is now open")


def close_db():
    """Close the database."""
    global _DB
    _DB.close()


def _start_query():
    global _DB

    query = QSqlQuery(_DB)
    query.exec_('PRAGMA foreign_keys=ON;')

    return query


def _create_new_ids_table(p_name):
    query = _start_query()

    # create new table, not always required
    cmd = 'CREATE TABLE {:s}_ids ( id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE );'.format(
        p_name)
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    # create temp table for copying PluginCollection, not always required
    rec = _DB.record("PluginCollection")
    col_names = [rec.fieldName(ii) for ii in range(rec.count())]
    fmt = '''CREATE TABLE _tmp (
        collection_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name VARCHAR(32)'''
    existing_fks = []
    for col in col_names:
        if col in ('collection_id', 'name'):
            continue
        fmt += ',\n{:8s}{:s} INTEGER UNIQUE DEFAULT NULL'.format('', col)
        existing_fks.append(col)

    new_fk = '{:s}_id'.format(p_name)
    fmt += ',\n{:8s}{:s} INTEGER UNIQUE DEFAULT NULL'.format('', new_fk)
    combined_fks = existing_fks + [new_fk, ]

    fk_fmt = ''
    for ii, col in enumerate(combined_fks):
        fk_fmt += ',\n{:8s}FOREIGN KEY ({:s}) REFERENCES {:s}s(id) ON UPDATE CASCADE ON DELETE CASCADE'.format(
            '', col, col)

    cmd = '{:s}{:s});'.format(fmt, fk_fmt)
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    # copy PluginCollection to temp table, not always required
    if len(existing_fks) > 0:
        joined = ', '.join(existing_fks)
        cmd = 'INSERT INTO _tmp(name, {:s}) SELECT name, {:s} FROM PluginCollection;'.format(
            joined, joined)
    else:
        cmd = 'INSERT INTO _tmp(name) SELECT name FROM PluginCollection;'
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    # drop PluginCollection table, not always required
    cmd = 'DROP TABLE PluginCollection;'
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    # rename temp table, not always required
    cmd = 'ALTER TABLE _tmp RENAME to PluginCollection;'
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())


def _create_name_id_data_table(p_name, p_id, schema_fields):
    query = _start_query()

    base = '''CREATE TABLE {:s}_{:d}_data (
        time_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        p_id INTEGER'''.format(p_name, p_id)
    tail = ''',
        FOREIGN KEY (p_id) REFERENCES {:s}_ids(id) ON UPDATE CASCADE ON DELETE CASCADE );'''.format(p_name)

    mid = ''
    for key, val in schema_fields:
        if val.lower() == 'int':
            dtype = 'INTEGER'
        elif val.lower() in ('float', 'double'):
            dtype = 'REAL'
        elif val.lower() == 'str':
            dtype = 'TEXT'
        else:
            msg = 'Database does not support data type {} from schema for plugin {}'
            logger.critical(msg.format(val, p_name))
            continue

        mid += ',\n{:8s}{:s} {:s}'.format('', key, dtype)

    cmd = '{:s}{:s}{:s}'.format(base, mid, tail)

    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())


def _add_new_id_val(p_name):
    query = _start_query()

    cmd = 'INSERT INTO {:s}_ids (id) VALUES (NULL);'.format(p_name)
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    cmd = 'SELECT LAST_VALUE(id) OVER (ORDER BY id DESC) FROM {:s}_ids'.format(
        p_name)
    logger.debug(cmd)
    query.exec_(cmd)

    query.first()
    return int(query.value(0))


def _add_new_pc_val(p_name, p_id):
    query = _start_query()

    cmd = 'INSERT INTO PluginCollection (name, {:s}_id) VALUES (\'{:s}\', {:d});'.format(
        p_name, p_name, p_id)
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())


def add_plugin(p_name):
    """Add a new plugin to the data base, account for multiple of the same name.

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

    if '{:s}_ids'.format(p_name) not in _DB.tables():
        # create new name_ids table
        _create_new_ids_table(p_name)

        # add new val to name_id table
        p_id = _add_new_id_val(p_name)

        # add new val to pc table
        _add_new_pc_val(p_name, p_id)

        # create name_id_data
        if '{:s}_{:d}_data'.format(p_name, p_id) not in _DB.tables():
            schema_fields = pluginMonitor.extract_schema_data_fields(p_name)
            _create_name_id_data_table(p_name, p_id, schema_fields)

    else:
        # add new val to name_id table
        p_id = _add_new_id_val(p_name)

        # add new val to pc table
        _add_new_pc_val(p_name, p_id)

        # create name_id_data
        if '{:s}_{:d}_data'.format(p_name, p_id) not in _DB.tables():
            schema_fields = pluginMonitor.extract_schema_data_fields(p_name)
            _create_name_id_data_table(p_name, p_id, schema_fields)

    return p_id


def remove_plugin(p_name, p_id):
    if '{:s}_ids'.format(p_name) in _DB.tables():
        query = _start_query()
        cmd = 'DELETE FROM {:s}_ids WHERE id = {:d}'.format(p_name, p_id)
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
        cmd = 'SELECT name FROM PluginCollection WHERE collection_id = {:d}'.format(
            c_id)
        logger.debug(cmd)
        res = query.exec_(cmd)
        if not res:
            logger.critical(query.lastError().text())
            break
        query.first()
        p_name = query.value(0)

        cmd = 'SELECT {:s}_id FROM PluginCollection WHERE collection_id = {:d}'.format(
            p_name, c_id)
        logger.debug(cmd)
        res = query.exec_(cmd)
        if not res:
            logger.critical(query.lastError().text())
            break
        query.first()
        p_id = int(query.value(0))

        if not remove_plugin(p_name, p_id):
            logger.critical(
                'Failed to completely remove Plugin: {} ID: {}'.format(p_name, p_id))


def add_plugin_data(p_name, p_id, data, schema):
    tbl = '{:s}_{:d}_data'.format(p_name, p_id)
    if tbl not in _DB.tables():
        return False

    query = _start_query()
    cmd = '''INSERT INTO {:s} (
        p_id'''.format(tbl)

    for key, val in schema:
        cmd += ',\n{:8s}{:s}'.format('', key)

    cmd += ''')\nVALUES (
        {:d}'''.format(p_id)

    for key, dtype in schema:
        if key not in data:
            logger.critical(
                'Missing {:s} in packet from Plugin: {:s} ID: {:d}'.format(key, p_name, p_id))
            return False

        if dtype == 'str':
            cmd += ',\n{:8s}''{}'''.format('', data[key])
        else:
            cmd += ',\n{:8s}{}'.format('', data[key])

    cmd += ');'
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())
        return False

    return True


def get_plugin_names(distinct):
    if distinct:
        extra = 'DISTINCT'
    else:
        extra = ''

    query = _start_query()
    cmd = 'SELECT {:s} name FROM PluginCollection'.format(extra)
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

    tbl = '{:s}_ids'.format(p_name)
    if tbl not in _DB.tables():
        logger.critical(
            'Failed to find id table for plugin {:s}'.format(p_name))
        return []

    cmd = 'SELECT id FROM {:s}'.format(tbl)
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


def get_drone_ids(distinct):
    if distinct:
        extra = ' DISTINCT'
    else:
        extra = ''

    query = _start_query()

    if _main_table not in _DB.tables():
        logger.critical("Unable to find {} in database".format(_main_table))

    cmd = 'SELECT {} name FROM {}'.format(extra, _main_table)
    result = query.exec_(cmd)

    # query.seek(-1)
    names = []
    while result and query.next():
        names.append(query.value(0))
    return names


def add_vehicle(name):

    query = _start_query()
    count = len(get_drone_ids(False))

    # adding to the main table
    cmd = 'INSERT into drone_collection (uid, name) VALUES ({}, "{}");'.format(count, name)
    logger.info("Adding vehicle {} into drone collection".format(name))
    res1 = query.exec_(cmd)

    # adding the rate tables
    table_name = create_drone_rate_table_name(name, DroneRates.RATE1)
    cmd = """CREATE TABLE IF NOT EXISTS {:s} (
     m_time float PRIMARY KEY,
     flt_mode integer,
     arm bool,
     gnss_fix integer,
     voltage float,
     current float,
     next_wp integer,
     tof float,
     relay_sw bool,
     engine_sw bool,
     connection bool
     );""".format(table_name)
    res2 = query.exec_(cmd)

    table_name = create_drone_rate_table_name(name, DroneRates.RATE2)
    cmd = """CREATE TABLE IF NOT EXISTS {:s} (
     m_time float PRIMARY KEY,
     roll_angle float,
     pitch_angle float,
     heading float,
     track float,
     vspeed float,
     gndspeed float,
     airspeed float,
     latitude float,
     longitude float,
     altitude float
     );""".format(table_name)
    res3 = query.exec_(cmd)

    if res1 and res2 and res3:
        return True


def remove_vehicle(name):

    query = _start_query()

    cmd = "DELETE FROM drone_collection WHERE name LIKE '%{}%';".format(name)
    res = query.exec_(cmd)
    if not res:
        logger.warning("Unable to delete {} from drone_collection".format(name))
    if res:
        logger.info("Deleted {} from done_collection".format(name))

    drop_rate1 = "DROP TABLE IF EXISTS {}".format(create_drone_rate_table_name(name, DroneRates.RATE1))
    drop_rate2 = "DROP TABLE IF EXISTS {}".format(create_drone_rate_table_name(name, DroneRates.RATE2))
    res_rate1 = query.exec_(drop_rate1)
    res_rate2 = query.exec_(drop_rate2)
    if res_rate1 and res_rate2:
        logger.info("Erased all parameters for {}".format(name))


def get_params(table_name, params):
    """Get parameters from the database.

    Returns
    -------
    dict
        dictionary of parameter keys and values
    """

    query = _start_query()
    req_params = ", ".join(params)
    cmd = "SELECT {} FROM {}".format(req_params, table_name)
    val = {}
    result = query.exec_(cmd)
    query.last()
    for param in params:
        val[param] = query.value(param)
    return val


def create_drone_rate_table_name(name, rate):
    return "{:s}_{:s}".format(name, rate)


def add_values(vals, table_name):
    """

    Parameters
    ----------
    vals : dict
        Set of flight data.
    table_name : str
        Table name of where to store data
        eg. drone0_rate1

    Returns
    -------
    None.

    """

    keys = ', '.join(list(vals.keys()))
    values = str(list(vals.values()))[1:-1]
    query = _start_query()
    cmd = "INSERT INTO {} ({}) VALUES ({});".format(table_name, keys, values)
    res = query.exec_(cmd)

    # if not res:
    #     logger.warning("Unable to add new values in the database")


def get_drone_name(uid):
    """Gives the vehicle name for corresponding uid. uid indexing starts from 0"""
    query = _start_query()
    cmd = "SELECT name FROM drone_collection WHERE uid = {};".format(uid)
    query.exec_(cmd)
    query.last()
    return query.value(0)


def write_values(flt_data):
    """
    Gets all data from the backend, sorts out vehicle's name and rates.
    Then, sends it to add_values() to write on the database'

    Parameters
    ----------
    flt_data : list
        List of dictionaries rate1 and rate2.

    Returns
    -------
    None.

    """

    for item in flt_data:
        rate = item['rate']
        for key, values in item.items():
            if type(key) is int:
                name = get_drone_name(key - 1)      # indexing in "drone_collection" starts from uid = 0.
                table_name = create_drone_rate_table_name(name, rate)
                add_values(values, table_name)


if __name__ == "__main__":
    pass
