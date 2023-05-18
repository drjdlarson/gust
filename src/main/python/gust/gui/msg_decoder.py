"""A common file for all message encodings and enums"""
import math

class MessageDecoder:
    """Decodes different message and enums"""

    @staticmethod
    def findType(x):
        """Vehicle Type:: MAV_TYPE
        # https://mavlink.io/en/messages/common.html#MAV_TYPE
        """
        if x == 1:
            ans = "Fixed Wing"
        elif x == 2:
            ans = "Quadrotor"
        elif x == 4:
            ans = "Helicopter"
        elif x == 10:
            ans = "Ground Rover"
        elif x == 13:
            ans = "Hexacopter"
        elif x == 14:
            ans = "Octacopter"
        elif x == 15:
            ans = "Tricopter"
        elif x in set(19, 20, 21, 22, 23, 24, 25):
            ans = "VTOL"
        else:
            ans = "General"
        return ans.upper()

    @staticmethod
    def findAutopilot(x):
        """Autopilot type: MAV_AUTOPILOT
        # https://mavlink.io/en/messages/common.html#enums"""
        if x == 3:
            ans = "ArduPilot"
        elif x == 4:
            ans = "OpenPilot"
        else:
            ans = "Generic AutoPilot"
        return ans.upper()

    @staticmethod
    def findState(x):
        """System Status:: MAV_STATE
        # https://mavlink.io/en/messages/common.html#enums"""
        if x == 1:
            ans = "Booting"
        elif x == 2:
            ans = "Calibrating"
        elif x == 3:
            ans = "Armed"
        elif x == 4:
            ans = "Active"
        elif x == 5:
            ans = "Critical"
        elif x == 6:
            ans = "Emergency"
        elif x == 7:
            ans = "PowerOff"
        elif x == 8:
            ans = "Terminating"
        elif x == 9:
            ans = "Unknown"
        else:
            ans = "Disarmed"
        return ans.upper()

    @staticmethod
    def findMode(x):
        """Flight Mode:: MAV_MODE
        # https://mavlink.io/en/messages/common.html#enums"""

        # It is encoded as a bitmask
        # getting the position of the first 1 from the right of 8-bits
        if int(x) == 0:
            return "NONE"

        x = int(x)
        pos_of_one = int(math.log2(x&-x) + 1)
        if pos_of_one == 2:
            ans = "Test"
        elif pos_of_one == 3:
            ans = "Auto"
        elif pos_of_one == 4:
            ans = "Guided"
        elif pos_of_one == 5:
            ans = "Stabilize"
        elif pos_of_one == 6:
            ans = "Simulation"
        elif pos_of_one == 7:
            ans = "Manual"
        else:
            ans = "None"
        return ans.upper()

    @staticmethod
    def findFix(x):
        """GNSS Fix Type (Following BFS enum convention)
        https://github.com/bolderflight/gnss/blob/main/include/gnss/gnss.h
        """
        if x == 1:
            ans = "NO Fix"
        elif x == 2:
            ans = "2D Fix"
        elif x == 3:
            ans = "3D Fix"
        elif x == 4:
            ans = "DGNSS Fix"
        elif x == 5:
            ans = "RTK Float"
        elif x == 6:
            ans = "RTK Fix"
        else:
            ans = "NO_FIX"
        return ans.upper()
