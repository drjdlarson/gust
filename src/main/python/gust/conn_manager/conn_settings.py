"""Define constants for data manager server/clients functions"""

IP = "127.0.0.1"
PORT = 9810
FORMAT = 'utf-8'
MAX_CONNECTIONS = 10
MAX_MSG_SIZE = 1500
TIMEOUT = 1

# messages
DISC_MSG = 'disconnect'
SUCC_MSG ='connected'

# message_type
DRONE_CONN = 'drone_connection'



def ADDR():
    return (IP, PORT)
