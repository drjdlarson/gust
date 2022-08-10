#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:48:32 2022

@author: lagerprocessor
"""
import json
import socket
import gust.conn_manager.conn_settings as conn_settings

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(conn_settings.ADDR)

def send(raw_msg):
    message = prepare_msg(raw_msg)
    msg_length = len(message)
    send_length = str(msg_length).encode(conn_settings.FORMAT)
    send_length += b' ' * (conn_settings.HEADER - len(send_length))

    client.send(send_length)
    client.send(message)

    msg = client.recv(conn_settings.HEADER).decode(conn_settings.FORMAT)
    return msg

def prepare_msg(msg):
    return json.dumps(msg).encode(conn_settings.FORMAT)


if __name__ == "__main__":

    send("Sending message to server")

    vehicle = {'name': 'SUPER-P3', 'port': '/dev/test/'}
    send(vehicle)
    # send(conn_settings.DISC_MSG)
