#!/bin/bash

startTime=$1
duration=$2
logPath=$3

echo "none" > $logPath/attack.txt
sleep $startTime
echo "forwarding" > $logPath/attack.txt
/sbin/sysctl -w net.ipv4.conf.all.forwarding=0
/sbin/sysctl -w net.ipv6.conf.all.forwarding=0
sleep $duration

/sbin/sysctl -w net.ipv4.conf.all.forwarding=1
/sbin/sysctl -w net.ipv6.conf.all.forwarding=1
