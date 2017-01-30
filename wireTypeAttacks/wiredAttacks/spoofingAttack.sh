#!/bin/bash 
startTime=$1
pendingDuration=$2
# Node is incremented by 10 based on scenario IP configuration
nodeToSpoof=`expr $3 + 10`
logPath=$4

# Parse routing protocol and convert to lowercase
routingProtocol=`echo $logPath | cut -d'_' -f7 | cut -d 'v' -f1 | sed 's/./\L&/g'`
subnet=`echo $logPath | cut -d '_' -f9`

cd "$SESSION_DIR/$NODE_NAME.conf"

echo "none" > $logPath/attack.txt
echo "sleep startime:" "$startTime"
sleep $startTime

#check for protocol
#if [[ $routingProtocol == *"ospf"* && -n "$5" && "IPv6" -eq "$5" ]]
#then
#	protocol="IPv6"
#	ipToSpoof="2001:""$nodeToSpoof""::1"	
	#start ospfv3
	##????
#	ifconfig eth0:1 inet6 add "$ipToSpoof/120" up
#else
protocol="IPv4" 
ipToSpoof="$nodeToSpoof.0.0.2"

cd "$SESSION_DIR/$NODE_NAME.conf"

sh quaggaboot.sh zebra
sh quaggaboot.sh "$routingProtocol"d
sh quaggaboot.sh vtysh

echo ifconfig eth0:1 $ipToSpoof netmask 255.255.255.$subnet up
ifconfig eth0:1 $ipToSpoof netmask 255.255.255.$subnet up
#fi
echo "$protocol" ":" "$ipToSpoof"
echo "starting spoof"
echo "spoof_"$ipToSpoof > $logPath/attack.txt

# Now check the routing protocol running  
cd var.run.quagga/
routingProcotolsRunning=`ls -1 | grep -v zebra.pid | grep pid | wc -l`	
if [ "$routingProcotolsRunning" -ne 1 ]
then
	echo "spoof_"$ipToSpoof "Error: Multiple Routing Procols Running -> $routingProcotolsRunning" > $logPath/attack.txt	
	echo "Multiple routing protocols"
	exit
fi

#if ospf is used
if [[ $routingProtocol == *"ospf"* ]]
then
	vtysh <<< $'configure terminal \n router ospf \n redistribute connected'
	echo "sent vtysh cmd"
fi

# attack duration
sleep $pendingDuration
#stop quagga
killall vtysh
killall "$routingProtocol"d
killall zebra

ifconfig "eth0:1" down
echo "eth0:1 down"

echo "none" > $logPath/attack.txt



