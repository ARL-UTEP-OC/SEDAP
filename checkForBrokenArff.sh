#!/bin/bash

cd /root/

for dir in `ls -d */`; do
	
	lines=`wc -l res.arff`
	
	if [ $lines -lt 90 ]
	then
		
		echo `pwd`
		cd ../
		
	fi
done
