"""Handle database operations."""
import os
import logging
from time import sleep

from PyQt5.QtSql import QSqlDatabase, QSqlQuery

DB_FILE = 'test_database.sqlite'
DB_PATH = './'
DB_DRIVER = "QSQLITE"

_DB = None

logger = logging.getLogger('[database]')

# TODO: make this thread safe

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

    # create database
    _DB = QSqlDatabase.addDatabase(DB_DRIVER)
    fpath = db_name()
    if os.path.exists(fpath):
        logger.debug('Removing existing database {}'.format(fpath))
        os.remove(fpath)
    _DB.setDatabaseName(fpath)
    _DB.open()

    query = _start_query()

    cmd = '''CREATE TABLE PluginCollection (
        collection_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        name VARCHAR(32) );'''
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())


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
    cmd = 'CREATE TABLE {:s}_ids ( id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE );'.format(p_name)
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
        fk_fmt += ',\n{:8s}FOREIGN KEY ({:s}) REFERENCES {:s}s(id) ON UPDATE CASCADE ON DELETE CASCADE'.format('', col, col)

    cmd = '{:s}{:s});'.format(fmt, fk_fmt)
    logger.debug(cmd)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    # copy PluginCollection to temp table, not always required
    if len(existing_fks) > 0:
        joined = ', '.join(existing_fks)
        cmd = 'INSERT INTO _tmp(name, {:s}) SELECT name, {:s} FROM PluginCollection;'.format(joined, joined)
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

    cmd = 'SELECT LAST_VALUE(id) OVER (ORDER BY id DESC) FROM {:s}_ids'.format(p_name)
    logger.debug(cmd)
    query.exec_(cmd)

    query.first()
    return int(query.value(0))


def _add_new_pc_val(p_name, p_id):
    query = _start_query()

    cmd = 'INSERT INTO PluginCollection (name, {:s}_id) VALUES (\'{:s}\', {:d});'.format(p_name, p_name, p_id)
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
        cmd = 'SELECT name FROM PluginCollection WHERE collection_id = {:d}'.format(c_id)
        logger.debug(cmd)
        res = query.exec_(cmd)
        if not res:
            logger.critical(query.lastError().text())
            break
        query.first()
        p_name = query.value(0)

        cmd = 'SELECT {:s}_id FROM PluginCollection WHERE collection_id = {:d}'.format(p_name, c_id)
        logger.debug(cmd)
        res = query.exec_(cmd)
        if not res:
            logger.critical(query.lastError().text())
            break
        query.first()
        p_id = int(query.value(0))

        if not remove_plugin(p_name, p_id):
            logger.critical('Failed to completely remove Plugin: {} ID: {}'.format(p_name, p_id))


def add_plugin_data(p_name, p_id, data):
    return True


def get_plugin_names(distinct):
    if distinct:
        extra = 'DISTINCT'
    else:
        extra = ''

    query = _start_query()
    cmd = 'SELECT {s} name FROM PluginCollection'.format(extra)
    res = query.exec_(cmd)
    if not res:
        logger.critical(query.lastError().text())

    query.first()

    plugin_names = []
    while query.next():
        plugin_names.append(query.value(0))

    return plugin_names
