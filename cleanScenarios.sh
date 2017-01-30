#!/bin/bash

# This script is resposnsible for checking for validity of folders created
# for scenarios. If scenarios created within root are corrupt, then the 
# folder will be deleted and created again recursively.

mainDir=$1

cd $mainDir 

# traverse through each directory and validate res.arff 
for dir in `ls -d */ | grep _sh`; do
	
	#cd $dir
	##lines=`cat res.arff | wc -l`
	##cd ../
	found=`find $dir -size 0`
	#echo $found
	##if [[ $lines -lt 40 && $dir == *"_sh"* ]]
	if [[ $found ]]
	then
	
		#if file is bad, then remove the directory
		rm -rf $dir
		echo "removing $dir"
	#else
	#	rename=`echo $dir | cut -d'*' -f1`
	#	mv $dir $rename
	fi
	
done
