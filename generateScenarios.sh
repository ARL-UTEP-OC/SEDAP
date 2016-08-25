#!/bin/bash

startTime=60

for scenario in "chainCoords" "cycleCoords" "treeCoords" "wheelCoords" "conn_grid" "starCoords" "two_centroidsCoords" 

do
	for protocol in "OLSR" "OSPFv3MDR"
	do
		for nodeNum in {1..10}
		do

			for attack in "spoofingAttack.sh1" "spoofingAttack.sh2" "spoofingAttack.sh3" "spoofingAttack.sh4" "spoofingAttack.sh5" "spoofingAttack.sh6" "spoofingAttack.sh7" "spoofingAttack.sh8" "spoofingAttack.sh9" "spoofingAttack.sh10" "forwardingAttack.sh" "blackholeAttack.sh" "downAttack.sh"
			do

				imnParams="$nodeNum $attack $scenario $protocol"
				echo $imnParams >> imnSets.txt

			done
		done
	done
done
