#!/bin/bash
scenario="jaime.scen"
startTime=60
numNodes=50
iterationsPerProtocol=100

for coordFile in "10x10.txt"

do
	for protocol in "OLSR" "OSPFv3MDR"
	do
		for nodeNum in {1..10}
		do


			for attack in "spoofingAttack.sh1" "spoofingAttack.sh2" "spoofingAttack.sh3" "spoofingAttack.sh4" "spoofingAttack.sh5" "spoofingAttack.sh6" "spoofingAttack.sh7" "spoofingAttack.sh8" "spoofingAttack.sh9" "spoofingAttack.sh10" "forwardingAttack.sh" "downAttack.sh"
			do
	imnName="$nodeNum"_"$startTime"_60_"$attack"_"$scenario"_"$protocol"_"$coordFile"
				echo $imnName
				imnName=${imnName//\./_}
				echo $imnName
			if [ ! -d /root/"$imnName" ]
			then

				rm /tmp/check.txt
				rm /tmp/wireshark*
				rm /tmp/maxn*		

				./imnGenerator.py $startTime 60 $numNodes $nodeNum $attack $scenario $protocol "$coordFile" > core/.core/configs/"$imnName".imn
				core-gui -s core/.core/configs/"$imnName".imn
			fi
			done
		done
	done
done
