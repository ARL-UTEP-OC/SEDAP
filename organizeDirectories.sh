#!/bin/bash

# This script is responsible for generating tar files in their 
# appropriate folder modules.

mainDir=$1
cd "$mainDir"

directoriesToTar=`ls $mainDir | grep "_sh"`

protocols=`cat protocols.txt`
attacks=`cat attacks.txt`
subnets=`cat subnets.txt`

for protocol in $protocols
do
	# check for existance of protocol directories
	if [ ! -d $protocol ]; then
	  mkdir $protocol
	fi
		
	for attack in $attacks
	do			
		for subnet in $subnets
		do
			# get rid of redundant names to avoid duplicates
			atk=`echo $attack | sed s/".sh".*/""/`
		
			if [ ! -d $protocol/$atk$subnet ]; then
				echo "making directory $atk$subnet"
				mkdir $protocol/$atk$subnet
			fi
		done
	done
done

# tar each scenario directory and place in proper folder modules
for dir in $directoriesToTar; do

	protocol=`echo $dir | cut -d'_' -f7`
	attack=`echo $dir | cut -d'_' -f4`
	subnet=`echo $dir | cut -d'_' -f9`

	cp -r $dir/ $protocol/$attack$subnet
	
done
