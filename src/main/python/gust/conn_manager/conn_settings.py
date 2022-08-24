"""Define constants for data manager server/clients functions"""

IP = "127.0.0.1"
PORT = 9810
FORMAT = 'utf-8'
MAX_CONNECTIONS = 10
MAX_MSG_SIZE = 1500
TIMEOUT = 1

# messages
DISC_MSG = 'disconnected'
SUCC_MSG ='connected'

# message_type
DRONE_CONN = 'drone_connect'
DRONE_DISC = 'drone_disconnect'



def ADDR():
    return (IP, PORT)
