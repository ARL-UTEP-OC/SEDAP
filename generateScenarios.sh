#!/bin/bash

startTime=60

for scenario in  "cycleCoords" "chainCoords" "treeCoords" "wheelCoords" "conn_grid" "starCoords" "two_centroidsCoords" 

do
	for protocol in "OLSR" "OSPFv3MDR"
	do
		for nodeNum in {1..10}
		do


			for attack in "spoofingAttack.sh3" "spoofingAttack.sh4" "spoofingAttack.sh5" "spoofingAttack.sh6" "spoofingAttack.sh7" "spoofingAttack.sh8" "spoofingAttack.sh9" "spoofingAttack.sh10" "forwardingAttack.sh" "blackholeAttack.sh" "downAttack.sh"
			do
				mobility=$scenario".scen"
				coordFile=$scenario".txt"
				imnName="$nodeNum"_"$startTime"_60_"$attack"_"$mobility"_"$protocol"_"$coordFile"
				
				imnName=${imnName//\./_}
				echo $imnName
				if [ ! -d /root/"$imnName" ]
				then

					rm /tmp/check.txt
					rm /tmp/wireshark*
					rm /tmp/maxn*		
					
					./imnGenerator.py $startTime 60 10 $nodeNum $attack $mobility $protocol "$coordFile" > core/.core/configs/"$imnName".imn
					core-gui -s core/.core/configs/"$imnName".imn
				fi
			done
		done
	done
done
