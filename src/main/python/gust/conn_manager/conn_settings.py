"""Define constants for data manager server/clients functions"""

IP = "127.0.0.1"
PORT = 9810
FORMAT = 'utf-8'
DISC_MSG = 'disconnect'
SUCC_MSG ='connected'
HEADER = 1024
MAX_CONNECTIONS = 10
MAX_MSG_SIZE = 1500
TIMEOUT = 1

def ADDR():
    return (IP, PORT)
