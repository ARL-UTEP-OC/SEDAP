#!/bin/bash

startTime=$1
duration=$2

sleep $startTime
echo "forwarding" > /tmp/attack.txt
/sbin/sysctl -w net.ipv4.conf.all.forwarding=0
/sbin/sysctl -w net.ipv6.conf.all.forwarding=0
sleep $duration

rm /tmp/attack.txt
/sbin/sysctl -w net.ipv4.conf.all.forwarding=1
/sbin/sysctl -w net.ipv6.conf.all.forwarding=1
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     