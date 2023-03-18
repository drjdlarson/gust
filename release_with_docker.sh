#!/bin/bash
# -------------------------------------------------------------------------------
# Make directories to share with containers
# -------------------------------------------------------------------------------
#mkdir -p repos/ardupilot_jetson
#mkdir -p repos/ardupilot_rpi
#mkdir -p repos/lager_sensors
#mkdir -p repos/fbs
mkdir -p build/jetson/target

# -------------------------------------------------------------------------------
# Initialize container emulation and start building/running the containers
# -------------------------------------------------------------------------------
#docker run --rm --privileged multiarch/qemu-user-static --reset -p yes --credential yes \
#  && ( (echo "Attempting to run containers..." && docker compose up) \
#      || (echo "Building containers and running..." && docker compose up --build && docker compose up) )

docker run --rm --privileged multiarch/qemu-user-static --reset -p yes --credential yes \
  && echo "Building containers and running..." && docker compose up --build && docker compose up