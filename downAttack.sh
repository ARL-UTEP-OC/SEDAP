#!/bin/bash

startTime=$1
duration=$2
logPath=$3

echo "none" > $logPath/attack.txt
sleep $startTime
echo "down" > $logPath/attack.txt
ifconfig eth0 down
sleep $duration

ifconfig eth0 up
