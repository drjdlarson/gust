#!/bin/bash
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes && docker-compose up --build