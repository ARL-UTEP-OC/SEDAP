#!/bin/bash

# This script is responsible for writing all possible permutations of
# nodes, protocols, scenarios, and attacks to a text file.


startTime=60

if [ -f imnSets.txt ]; then
    rm imnSets.txt
fi

for nodeNum in {1..10}
do
	for protocol in "OLSR" "OSPFv3MDR"
	do
		for scenario in "chainCoords" "cycleCoords" "treeCoords" "wheelCoords" "conn_grid" "starCoords" "two_centroidsCoords" 
		do

			for attack in "spoofingAttack.sh1" "spoofingAttack.sh2" "spoofingAttack.sh3" "spoofingAttack.sh4" "spoofingAttack.sh5" "spoofingAttack.sh6" "spoofingAttack.sh7" "spoofingAttack.sh8" "spoofingAttack.sh9" "spoofingAttack.sh10" "forwardingAttack.sh" "blackholeAttack.sh" "downAttack.sh"
			do
				# search for attacking node within attack type (spoofing)
				attackNumber="${attack//[^0-9]/}"

				# make sure victim and attacker aren't the same
				if [[ ! "$nodeNum" -eq "$attackNumber" ]]
				then
					imnParams="$nodeNum $attack $scenario $protocol"
					echo $imnParams >> imnSets.txt
				fi
				
			done
		done
	done
done
