#!/bin/bash

# This script is responsible for being the controller of running automatic
# data collection for parallel CORE scenarios.
#
# NOTE: Be sure to run flow generator script with appropriate amount of 
# 		nodes and wireType before running this script. ex) ./flowGenerator 10 wired 
# Usage: ./sedap param1 param2 param3
#		 param1 is the wire type. May be "wired" or "wireless"
#		 param2 is the amount of CORE instances to run at once.
#		 param3 is a "gui" parameter. If anything other than "gui" is entered, 
#		 the CORE gui will be killed after the creation of parallel CORE scenarios.
#		 #NOTE: param3 is broken->For future implementation.

wireType=$1
maxProcs=$2
gui=$3
imnFile=$wireType"ImnSets.txt"
scriptDir=`pwd`

# must change to this directory in order to run scripts
writingDir="/root/"$wireType

cd /root/
if [ ! -d $wireType ]					
then	
	mkdir $wireType
fi

#---------- Begin: Initialization of files to be read -----------#
cd "$scriptDir/flowGenerator"
./flowGenerator_3Nodes.py 10 $wireType #Script and number of nodes may be changed
cd $scriptDir
./generateScenarios.sh $wireType

imnTextFile=$scriptDir/$imnFile

#---------- End: Initialization of files to be read -----------#

#count number of current scenarios created to amount needed
permutations=`cat $imnTextFile | wc -l`
scenarioFolders=`ls /$writingDir/ | grep "_sh" | wc -l`

until [ $scenarioFolders -eq $permutations ]; do

	echo "Starting new set"

	# if there are still scenarios to be ran, then call parallelscenarios again
	cd $scriptDir
	./parallelScenarios.sh $imnTextFile $maxProcs $wireType $gui
	
	cd $scriptDir
	./cleanScenarios.sh $writingDir
	
	permutations=`cat $imnTextFile | wc -l`
	echo $permutations
	scenarioFolders=`ls $writingDir | grep "_sh" | wc -l`
	echo $scenarioFolders
done

# called to copy directories to appropriate locations for tar
cd $scriptDir
./organizeDirectories.sh $writingDir

cd $writingDir
# Removing for accurate file to be generated for each attack
if [ -f all.arff ]; then
    rm $writingDir/all.arff
fi

protocolDirectories=`ls $writingDir | grep -v "_sh" | grep -iE 'OLSR|OSPF|RIP'`

for protocolDir in $protocolDirectories
do

	cd $protocolDir
	for attackDir in `ls`; do

		if [[ $attackDir != *"tar"* ]]
		then
		
			cd $scriptDir
			# exececute runalltoarff.sh for generation of acurate all.arff files
			./runAllToArff.sh $writingDir/$protocolDir/$attackDir/ $wireType 
			
			cd $writingDir/$protocolDir/
			tar -cf $attackDir.tar $attackDir
			rm -rf $attackDir
		fi
		
	done
	
	cd ../
	
done
