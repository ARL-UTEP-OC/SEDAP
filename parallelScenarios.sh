#!/bin/bash

# This script is responsible for executing all scenarios within a specified
# text file. Scenarios will be executed in parallel by a specified number
# at a time.

imnFile=$1
maxProcs=$2
startTime=60
mainDir="root"

#read through each line of the text file
while IFS='' read -r imnString || [[ -n "$imnString" ]];
do 
	#convert to array
	imnParams=($imnString)

	nodeNum=${imnParams[0]}
	attack=${imnParams[1]}
	scenario=${imnParams[2]}
	protocol=${imnParams[3]}
					
	mobility=$scenario".scen"
	coordFile=$scenario".txt"
	
	#name of file to be created is based on parameters passed in
	imnName="$nodeNum"_"$startTime"_60_"$attack"_"$mobility"_"$protocol"_"$coordFile"
	imnName=${imnName//\./_}				

	#check for existance of scenario to avoid unnecessary overwriting
	if [ ! -d /$mainDir/$imnName ]					
	then	
					
		./imnGenerator.py $startTime 60 10 $nodeNum $attack $mobility $protocol "$coordFile" > core/.core/configs/$imnName.imn
		path=core/.core/configs/$imnName.imn
		
		#start core with the specified file and sleep for one second
		core-gui --start $path &
		sleep 1
		
	fi
	
	
	currentProcs=`pgrep -c wish`
	
	#compare current processes to amount of max processes allowed
	if [[ $currentProcs -ge $maxProcs ]]
	then
	
		#wait until all jobs have finished until starting more
		newestJob=`pgrep -n wish`
		wait $newestJob
		
		#to avoid using excess memory, cleanup files before continuing
		if grep -q SomeString "$File"; then
			rm /tmp/wireshark*
		fi
		
		if grep -q SomeString "$File"; then
			rm /tmp/maxn*	
		fi
		
	fi
					
done < "$imnFile"


