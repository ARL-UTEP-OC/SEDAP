#!/bin/bash 

# Teminates emulation
# First gets the process id of the newest created gui then
# it looks for the session id

sleeptime=$1
sleep 3
newstJob=$(pgrep -n wish)
pidnode=$(pgrep -n vnoded)
sessionid=$(ps x | grep $pidnode | awk 'print $8}' | cut -d'.' -f2 | cut -d'/' -f1)
sleep $sleeptime
core-gui -c $sessionid
kill -9 $newstJob
