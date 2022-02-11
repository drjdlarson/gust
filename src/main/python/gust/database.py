from PyQt5.QtSql import QSqlDatabase

DB_NAME = 'test_database'
DB_PATH = './'

def connect_to_database(driver=None, con_name=None):
    if driver is None:
        driver = "QSQLITE"

    if con_name is not None:
        args = (con_name, )
    else:
        args = ()

    db_name = DB_PATH + DB_NAME
    con = QSqlDatabase.addDatabase(driver, *args)
    con.setDatabaseName(db_name)

    return con


def open_database(connection):
    res = connection.open()

    if not res:
        err = connection.lastError().text()
    else:
        err = None

    return res, None
