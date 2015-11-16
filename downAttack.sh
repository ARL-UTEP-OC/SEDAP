#!/bin/bash

startTime=$1
duration=$2

echo "none" > /tmp/attack.txt
sleep $startTime
echo "down" > /tmp/attack.txt
ifconfig eth0 down
sleep $duration

ifconfig eth0 up
rm /tmp/attack.txt

