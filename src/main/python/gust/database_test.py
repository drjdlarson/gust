"""Handle database on the frontend side"""

import os
import logging
from time import sleep
import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

DB_FILE = 'dummy_drones.sqlite'
DB_PATH = './'
# DB_PATH = '~Projects/gust/src/main/resources/base/'
DB_DRIVER = 'QSQLITE'

_DB = None

logger = logging.getLogger('[database_test]')
logger.setLevel(logging.DEBUG)

logging.critical("this is critical log")


def db_name():

    global DB_FILE, DB_FILE
    return os.path.join(DB_PATH, DB_FILE)


def open_db():

    global _DB
    _DB = QSqlDatabase.addDatabase(DB_DRIVER)
    f_path = db_name()
    _DB.setDatabaseName(f_path)
    _DB.open()
    logger.info('Opening database...')

    if not _DB.open():
        logger.critical("Unable to open database")
        sys.exit()

    if _DB.open():
        logger.info("Database is open")


def _start_query():
    global _DB
    query = QSqlQuery()
    return query

def add_vehicle(name):

    query = _start_query()
    cmd = 'INSERT into drone_collection (uid, name) VALUES (3, "{}");'.format(name)

    logger.info("adding vehicle {} into drone collection".format(name))
    res = query.exec_(cmd)

    if not res:
        logger.critical("Unable to add {} into drone_collection".format(name))

def drone_id():

    query = _start_query()
    table_name = "drone_collection"

    if table_name not in _DB.tables():
        logger.critical("Unable to find {} in database".format(table_name))
        sys.exit()

    cmd = 'SELECT name FROM {}'.format(table_name)

    logger.debug("So, it is in the table")
    result = query.exec_(cmd)

    query.seek(-1)
    names = []
    while query.next():
        names.append(query.value(0))

    print(names)

""" Testing stuff"""
if __name__ == "__main__":

    open_db()

    # add_vehicle("QUESO")

    drone_id()

    _DB.close()
