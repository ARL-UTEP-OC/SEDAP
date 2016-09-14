#!/bin/bash

# This script is resposnsible for checking for validity of folders created
# for scenarios. If scenarios created within root are corrupt, then the 
# folder will be deleted and created again recursively.

mainDir="/root/"

cd $mainDir 

# traverse through each directory and validate res.arff 
for dir in `ls -d */`; do
	
	cd $dir
	lines=`cat res.arff | wc -l`
	cd ../
	
	if [[ $lines -lt 40 && $dir == *"_sh"* ]]
	then
	
		#if file is bad, then remove the directory
		rm -rf $dir
		echo "removing $dir"
		
	fi
	
done



