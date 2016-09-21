#!/bin/bash

# must change to this directory in order to run scripts
writingDir="/root"

scriptDir="/root/install/sedap/IntelAttacker"

#---------- Begin: Hard-coded section to be removed later -----------#
cd $scriptDir
./generateScenarios.sh

imnTextFile=$scriptDir"/imnSets.txt"
maxProcs=1
#---------- End: Hard-coded section to be removed later -----------#

#count number of current scenarios created to amount needed
permutations=`cat $imnTextFile | wc -l`
scenarioFolders=`ls /root/ | grep "_sh" | wc -l`


until [ $scenarioFolders -eq $permutations ]; do

	echo "Starting new set"

	# if there are still scenarios to be ran, then call parallelscenarios again
	#cd $scriptDir
	./parallelScenarios.sh $imnTextFile $maxProcs
	
	# ran to provide file for cleanscenarios script to check
	cd $scriptDir
	./runAllToArff.sh $writingDir
	
	# clears bad scenario folders
	cd $scriptDir
	./cleanScenarios.sh
	
	permutations=`cat $imnTextFile | wc -l`
	scenarioFolders=`ls $writingDir | grep "_sh" | wc -l`
	
done

# called to copy directories to appropriate locations for tar
cd $scriptDir
./organizeDirectories.sh

cd $writingDir
# Removing for accurate file to be generated for each attack
if [ -f all.arff ]; then
    rm $writingDir/all.arff
fi

protocolDirectories=`ls $writingDir | grep -v "_sh" | grep -E 'OLSR|OSPF'`

for protocolDir in $protocolDirectories
do

	cd $protocolDir
	for attackDir in `ls`; do

		if [[ $attackDir != *"tar"* ]]
		then
		
			cd $scriptDir
			# exececute runalltoarff.sh for generation of acurate all.arff files
			./runAllToArff.sh $writingDir/$protocolDir/$attackDir/ # ex) root/OLSR/spoofingAttack
			
			cd $writingDir/$protocolDir/
			tar -cf $attackDir.tar $attackDir
			rm -rf $attackDir
		fi
		
	done
	
	cd ../
	
done
