#!/bin/bash

startTime=60

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

