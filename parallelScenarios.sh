#!/bin/bash

# This script is responsible for executing all scenarios within a specified
# text file. Scenarios will be executed in parallel by a specified number
# at a time.

imnFile=$1
maxProcs=$2
wireType=$3
gui=$4
startTime=60
mainDir="root"/$wireType

#read through each line of the text file
while IFS='' read -r imnString || [[ -n "$imnString" ]];
do 
	#convert to array
	imnParams=($imnString)

	nodeNum=${imnParams[0]}
	attack=${imnParams[1]}
	scenario=${imnParams[2]}
	protocol=${imnParams[3]}
	subnet=${imnParams[4]}

	#name of file to be created is based on parameters passed in
	imnName="$nodeNum"_"$startTime"_60_"$attack"_"$scenario"_"$protocol"_"$wireType"
	imnName=${imnName//\./_}
	imnName+=_"$subnet"
	echo $imnName
	#check for existance of scenario to avoid unnecessary overwriting
	if [[ ! -d /$mainDir/$imnName ]]					
	then
		# first make a copy of the file to be modified
		path=core/.core/configs/$imnName.imn
		cat staticScenarios/"$wireType"_scenarios/"$scenario".imn > $path
		./imnGenerator.py $startTime 60 10 $nodeNum $attack $scenario $protocol $wireType $path $subnet

		#start core with the specified file and sleep for one second
		#core-gui --batch $path
		core-gui --start $path &
		sleep 10s
		
	fi
	
	currentProcs=`ps aux | grep -v grep | grep -c "n1 -l"`
	permutations=`cat $imnFile | wc -l`
	scenarioFolders=`ls /$mainDir/ | grep -c "_sh"
	scenariosLeft=`expr $permutations - $scenarioFolders`
	tempMaxProcs=$maxProcs
	if [[ $scenariosLeft -lt $maxProcs ]]
	then
		maxProcs=$scenariosLeft
	fi
	
	#compare current processes to amount of max processes allowed
	if [[ $currentProcs -ge $maxProcs ]]
	then
		if [ "$gui" != "gui" ]
		then
			killall wish8.5
		fi
		
		# Call script to wait for specified runtime and then kill all processes
		./terminateSessions.sh 180
		sleep 3
		
		
		#to avoid using excess memory, cleanup files before continuing
		rm /tmp/wireshark*
		rm /tmp/maxn*	

	fi
	
	maxProcs=$tempMaxProcs
			
done < "$imnFile"


