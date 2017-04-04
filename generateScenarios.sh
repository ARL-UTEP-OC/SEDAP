#!/bin/bash

# This script is responsible for writing all possible permutations of
# nodes, protocols, scenarios, and attacks to a text file.

# Pass "wired" or "wireless" for type of emulation
wireType=$1 
startTime=60
attacks="blackholeAttack.sh spoofingAttack.sh1 spoofingAttack.sh2 spoofingAttack.sh3 spoofingAttack.sh4 spoofingAttack.sh5 spoofingAttack.sh6 spoofingAttack.sh7 spoofingAttack.sh8 spoofingAttack.sh9 spoofingAttack.sh10"
protocols="OSPFv2 RIP" # Protocol is initially based on wired scenarios. BGP to be added
scenarios="chain cycle tree wheel conn-grid star two-centroids"
subnets="255.255.255.255" #"255.255.255.128 255.255.255.0 255.255.0.0 255.255.255.255" #only 255 for first wireless run

# Protocols and Attacks will be modified based on wire type
if [ $wireType == "wireless" ]
then
    #attacks+=" downAttack.sh forwardingAttack.sh"
    protocols="OLSR OSPFv3MDR"
fi

echo $protocols > "/root/$wireType/protocols.txt"
echo $attacks > "/root/$wireType/attacks.txt"
echo $subnets > "/root/$wireType/subnets.txt"

if [ -f $wireType"ImnSets.txt" ]
then
    rm $wireType"ImnSets.txt"
fi

#for nodeNum in 10
#do
	for protocol in $protocols
	do
		for scenario in $scenarios
		do
			for attack in $attacks
			do
				for subnet in $subnets
				do
					# search for attacking node within attack type (spoofing)
					attackNumber="${attack//[^0-9]/}"
	
					# make sure victim and attacker aren't the same
					if [[ ! "$nodeNum" -eq "$attackNumber" ]]
					then
						imnParams="10 $attack $scenario $protocol $subnet"
						echo $imnParams >> $wireType"ImnSets.txt"
					fi
				done
			done
		done
	done
#done
