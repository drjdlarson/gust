"""Handle database on the frontend side"""

import os
import logging
from time import sleep
import sys
import enum

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

DB_FILE = 'dummy_drones.sqlite'
DB_PATH = '/home/lagerprocessor/Projects/gust/src/main/resources/base/'
DB_DRIVER = 'QSQLITE'

_DB = None
_main_table = "drone_collection"

_rate1_table = 'rate1'
_rate2_table = 'rate2'

@enum.unique
class DroneRates(enum.Enum):

    RATE1 = enum.auto()
    RATE2 = enum.auto()

    def __str__(self):
        return self.name.lower()

logger = logging.getLogger('[database_test]')
logger.setLevel(logging.DEBUG)


def db_name():

    global DB_FILE, DB_FILE
    return os.path.join(DB_PATH, DB_FILE)


def open_db():

    global _DB
    if _DB is not None:
        return
    _DB = QSqlDatabase.addDatabase(DB_DRIVER)
    f_path = db_name()
    _DB.setDatabaseName(f_path)
    _DB.open()
    logger.info('Opening database...')

    if not _DB.open():
        logger.critical("Unable to open database")

    if _DB.open():
        logger.info("Database is open")


def _start_query():
    global _DB
    query = QSqlQuery(_DB)
    return query


def get_drone_ids(distinct):
    if distinct:
        extra = ' DISTINCT'
    else:
        extra = ''

    query = _start_query()

    if _main_table not in _DB.tables():
        logger.critical("Unable to find {} in database".format(_main_table))
        sys.exit()

    cmd = 'SELECT {} name FROM {}'.format(extra, _main_table)
    result = query.exec_(cmd)

    # query.seek(-1)
    names = []
    while query.next():
        names.append(query.value(0))
    return names


def add_vehicle(name):

    query = _start_query()
    count = len(get_drone_ids(False))

    # adding to the main table
    cmd = 'INSERT into drone_collection (uid, name) VALUES ({}, "{}");'.format(count, name)
    logger.info("Adding vehicle {} into drone collection".format(name))
    res = query.exec_(cmd)

    if not res:
        logger.critical("Unable to add {} into drone_collection".format(name))

    # adding the rate tables
    table_name = "{:s}_{:s}".format(name, _rate1_table)
    cmd = """CREATE TABLE IF NOT EXISTS {:s} (
     m_time float PRIMARY KEY,
     flt_mode integer,
     arm_state bool,
     voltage float,
     current float,
     next_wp integer,
     time_of_flight float,
     relay_switch bool,
     engine_switch bool,
     connection_status bool
     );""".format(table_name)
    query.exec_(cmd)

    table_name = "{:s}_{:s}".format(name, _rate2_table)
    cmd = """CREATE TABLE IF NOT EXISTS {:s} (
     m_time float PRIMARY KEY,
     roll float,
     pitch float,
     heading float,
     track float,
     vspeed float,
     gndspeed float,
     airspeed float,
     latitutde float,
     longitude float,
     altitude float
     );""".format(table_name)
    query.exec_(cmd)


def remove_vehicle(name):

    query = _start_query()

    cmd = "DELETE FROM drone_collection WHERE name LIKE '%{}%';".format(name)
    res = query.exec_(cmd)
    if not res:
        logger.warning("Unable to delete {} from drone_collection".format(name))
    if res:
        logger.info("Deleted {} from done_collection".format(name))

    drop_rate1 = "DROP TABLE IF EXISTS {}_rate1".format(name)
    drop_rate2 = "DROP TABLE IF EXISTS {}_rate2".format(name)
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


""" Testing stuff"""
if __name__ == "__main__":

    flight_data = {}

    open_db()
    # add_vehicle("savage")
    names = get_drone_ids(True)
    # remove_vehicle('savage')
    print(get_drone_ids(True))

    # res = {}
    # req_params = ['voltage', 'current']
    # for index, name in enumerate(names):
    #     table_name = "{}_rate1".format(name)
    #     params = 'voltage'
    #     # params = ', '.join(req_params)
    #     print(get_params(params, table_name))
    # print(res)

    sys_data = {}
    for index, drone in enumerate(names):
        table_name = "{}_rate1".format(drone)
        query = _start_query()
        params = ['voltage', 'current']
        key = index + 1
        sys_data[key] = get_params(table_name, params)


    # query = _start_query()
    # params = ['voltage', 'current']
    # table_name = "drone0_rate1"
    # sys_data = get_params(table_name, params)
    print(sys_data)
    _DB.close()
    sys.exit()
