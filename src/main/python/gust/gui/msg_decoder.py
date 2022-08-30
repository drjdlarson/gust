import math

class MessageDecoder:

    @staticmethod
    def findType(x):
        if x == 1:
            return "Fixed Wing"
        elif x == 2:
            return "Quadrotor"
        elif x == 4:
            return "Helicopter"
        elif x == 10:
            return "Ground Rover"
        elif x == 13:
            return "Hexacopter"
        elif x == 14:
            return "Octacopter"
        elif x == 15:
            return "Tricopter"
        elif x in set(19, 20, 21, 22, 23, 24, 25):
            return "VTOL"
        else:
            return "General"

    @staticmethod
    def findAutopilot(x):
        if x == 3:
            return "ArduPilot"
        elif x == 4:
            return "OpenPilot"
        else:
            return "Generic AutoPilot"

    @staticmethod
    def findState(x):
        if x == 1:
            return "Booting"
        elif x == 2:
            return "Calibrating"
        elif x == 3:
            return "Armed"
        elif x == 4:
            return "Active"
        elif x == 5:
            return "Critical"
        elif x == 6:
            return "Emergency"
        elif x == 7:
            return "PowerOff"
        elif x == 8:
            return "Terminating"
        else:
            return "Unknown"

    @staticmethod
    def findMode(x):
        # getting the position of the first 1 from the right of 8-bits
        x = int(x)
        pos_of_one = int(math.log2(x&-x) + 1)

        if pos_of_one == 2:
            return "Test"
        elif pos_of_one == 3:
            return "Auto"
        elif pos_of_one == 4:
            return "Guided"
        elif pos_of_one == 5:
            return "Stabilize"
        elif pos_of_one == 6:
            return "Simulation"
        elif pos_of_one == 7:
            return "Manual"
        else:
            return "None"

    @staticmethod
    def findFix(x):
        if x == 2:
            return "2D Fix"
        elif x == 3:
            return "3D Fix"
        else:
            return "No Fix"
