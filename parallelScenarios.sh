#!/bin/bash

imnFile=$1
maxProcs=$2
startTime=60

rm /tmp/wireshark*
rm /tmp/maxn*	


while IFS='' read -r imnString || [[ -n "$imnString" ]];
do 
		
	imnParams=($imnString)

	nodeNum=${imnParams[0]}
	attack=${imnParams[1]}
	scenario=${imnParams[2]}
	protocol=${imnParams[3]}
					
	mobility=$scenario".scen"
	coordFile=$scenario".txt"
					
	imnName="$nodeNum"_"$startTime"_60_"$attack"_"$mobility"_"$protocol"_"$coordFile"
	imnName=${imnName//\./_}				


	if [ ! -d /root/"$imnName" ]					
	then	
					
		./imnGenerator.py $startTime 60 10 $nodeNum $attack $mobility $protocol "$coordFile" > core/.core/configs/"$imnName".imn
		path=core/.core/configs/"$imnName".imn
		core-gui --start $path &
		sleep 1 
	fi
	
	
	currentProcs=`pgrep -c wish`
	
	if [[ $currentProcs -ge $maxProcs ]]
	then
		oldestJob=`pgrep -o wish`
		wait $oldestJob
	fi
					
done < "$imnFile"
