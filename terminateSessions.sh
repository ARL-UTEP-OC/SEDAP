#!/bin/bash

# Terminates emulation
# First gets the proces id of the newest created gui then
# it looks for the session id

sleeptime=$1
sleep 3

sessionIDs=`core-gui -c | grep "list:" | cut -d':' -f3`
sleep $sleeptime

for id in $sessionIDs
do
	echo "Killing core session: $id"
	core-gui -c $id
done

echo "Killing core GUI"
killall wish8.5
