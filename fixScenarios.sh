#!/bin/bash

inputFile=$1
maxProcs=$2


cd /root/


for dir in `ls -d */`; do
	
	cd $dir
	lines=`cat res.arff | wc -l`
	cd ../
	
	if [[ $lines -lt 40 && $dir == *"_sh"* ]]
	then
	

		rm -rf $dir
		echo "removing $dir"
		
	fi
	
done

permutations=`wc -l < /root/install/sedap/IntelAttacker/$inputFile`
scenarioFolders=`ls /root/ | grep "_sh" | wc -l`

if [[ $scenarioFolders -lt $permutations ]]
then

	echo "Starting new set"
	cd /root/install/sedap/IntelAttacker/
	./parallelScenarios.sh $inputFile $maxProcs
	
fi

