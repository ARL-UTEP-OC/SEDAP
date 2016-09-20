#!/bin/bash

# This script is responsible for generating tar files in their 
# appropriate folder modules.

mainDir="/root/"
cd "$mainDir"

directoriesToTar=`ls $mainDir | grep "_sh"`

olsrDir="OLSR"
ospfDir="OSPFv3MDR"

spoof="spoofingAttack"
down="downAttack"
blackhole="blackholeAttack"
forwarding="forwardingAttack"

# check for existance of protocol directories
if [ ! -d $olsrDir ]; then
  
  mkdir $olsrDir
  mkdir $olsrDir/$spoof
  mkdir $olsrDir/$down
  mkdir $olsrDir/$blackhole
  mkdir $olsrDir/$forwarding
  
fi

if [ ! -d $ospfDir ]; then
  
  mkdir $ospfDir
  mkdir $ospfDir/$spoof
  mkdir $ospfDir/$down
  mkdir $ospfDir/$blackhole
  mkdir $ospfDir/$forwarding
  
fi

# tar each scenario directory and place in proper folder modules
for dir in $directoriesToTar; do

	protocol=$olsrDir
	
	if [[ $dir == *"OSPF"* ]]
	then
	
		protocol=$ospfDir
		
	fi
	
	attack=`echo $dir | cut -f4,4 -d'_'`
	cp -r $dir/ $protocol/$attack/
	
done

