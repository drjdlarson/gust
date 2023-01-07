#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 12:40:47 2022

@author: lagerprocessor
"""

import dronekit
import time
from pymavlink import mavutil

print("Connecting to the vehicle...")
ale = dronekit.connect('/dev/ttyUSB0', wait_ready = True, baud=57600)
print('Connection successful!')

cmds = ale.commands

print('preparing the first command')
fseq = 0
fcurrent_wp = 1
fframe = 0
fcommand = 16
fparam1 = 0
fparam2 = 0
fparam3 = 0
fparam4 = 0
flat = 1
flon = 1
falt = 0
fautocontinue = 1
cmd1 = dronekit.Command(ale._handler.target_system, 0, fseq, fframe, fcommand, 0, 0, fparam1, fparam2, fparam3, fparam4, flat, flon, falt)

print('Adding the first command')
cmds.add(cmd1)

print('preparing second command')

seq = 1
current_wp = 0
frame = 3
command = 16
param1 = 1
param2 = 0
param3 = 0
param4 = 0
lat = 37
lon = -80
alt = 100
autocontinue = 1
cmd2 = dronekit.Command(ale._handler.target_system, 0, seq, frame, command, 0, 0, param1, param2, param3, param4, lat, lon, alt)

print('Adding the second command')
cmds.add(cmd2)

print('Uploading the two waypoints')

if cmds._vehicle._wpts_dirty:
    print("_wpts_dirty is True")
    cmds._vehicle._master.waypoint_clear_all_send()
    start_time = time.time()
    if cmds._vehicle._wploader.count() > 0:
        print("_wploder.count > 1")
        cmds._vehicle._wp_uploaded = [False] * cmds._vehicle._wploader.count()
        cmds._vehicle._master.waypoint_count_send(cmds._vehicle._wploader.count())
        print("_wploder.count > 1")
        while False in cmds._vehicle._wp_uploaded:
            time.sleep(0.5)
            print("Waiting to upload completed")



print('Successfully uploaded!')