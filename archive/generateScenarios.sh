#!/bin/bash
scenario="sample4.scen"
numReps=5

for startTime in {10..180..60}
do
	for protocol in "OLSR" "OSPFv3MDR"
	do
		for nodeNum in {1..10}
		do


			for attack in "forwardingAttack.sh" "spoofing1Attack.sh" "spoofing2Attack.sh" "spoofing3Attack.sh" "spoofing4Attack.sh" "spoofing5Attack.sh"  
			do
	imnName="$nodeNum"_"$startTime"_60_"$attack"_"$scenario"_"$protocol"
				echo $imnName
				imnName=${imnName//\./_}
				echo $imnName
			if [ ! -d /root/"$imnName"_"$numReps" ]
			then
				#do each 5 times
				for ((rep=1;rep<=$numReps;rep++))
				do
				rm /tmp/check.txt
				rm /tmp/wiresharkX*
				rm /tmp/maxn*
				

				./imnGenerator.py $startTime 60 10 $nodeNum $attack $scenario $protocol > /home/core/.core/configs/"$imnName".imn
				/usr/bin/core -s /home/core/.core/configs/"$imnName".imn
				mv /root/"$imnName" /root/"$imnName"_"$rep"
				done

				rm /tmp/check.txt
				rm /tmp/wiresharkX*
				rm /tmp/maxn*
			else
				echo "Skipping config $imnName because folder already exists"
			fi
			done
		done
	done
done
