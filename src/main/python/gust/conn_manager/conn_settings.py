"""Define constants for data manager server/clients functions"""

# %% Settings
IP = "127.0.0.1"
PORT = 9810
FORMAT = 'utf-8'
MAX_CONNECTIONS = 10
MAX_MSG_SIZE = 1500
TIMEOUT = 10
RADIO_PORTS = [9820, 9830, 9840, 9850, 9860]

# messages, not used?
# DISC_MSG = 'disconnected'
# SUCC_MSG ='connected'

# %% DRONE message_type
DRONE_CONN = 'drone_connect'
DRONE_DISC = 'drone_disconnect'

# %% ZED message_type
ZED_CONN = 'zed_connect'


# %% Helper functions
def ADDR():
    return (IP, PORT)
