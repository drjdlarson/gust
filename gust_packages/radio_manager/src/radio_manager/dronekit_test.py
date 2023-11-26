"""For Testing Purposes Only"""
import time
import argparse
import dronekit

parser = argparse.ArgumentParser(
    description="Test getting data from a radio module over MAVlink using Dronekit"
)
parser.add_argument("addr", type=str, help="Hardware address of the radio")
parser.add_argument("baud", type=int, help="Baud rate of the radio")

args = parser.parse_args()

# connecting to the vehicle.
vehicle = dronekit.connect(args.addr, baud=args.baud, wait_ready=True)


@vehicle.on_message("*")
def listener(name, message):
    print("message::>>{}".format(message))
