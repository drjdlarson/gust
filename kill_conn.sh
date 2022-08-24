#! /bin/bash
lsof -i:9810
echo "pid"
read pid
kill -9 $pid
