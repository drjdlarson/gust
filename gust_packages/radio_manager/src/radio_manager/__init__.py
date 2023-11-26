"""Handles dronekit connection with the vehicle
Includes methods to send/receive MAVLink messages.
Used for both hardware and SIL connections."""

import logging

logger = logging.getLogger(__name__)
logging.getLogger(__name__).addHandler(logging.NullHandler())
