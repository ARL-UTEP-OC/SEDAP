#!/bin/bash

for dir in `ls -d */`
do
	cd $dir
	file="n"`echo $dir | cut -d'_' -f1`".capture"
	echo "in $dir looking in "$file
	unique=`cat $file | cut -d';' -f6 | uniq`
	echo "$dir",`echo $unique | tr '\n\r ' ','`

	cd ..
	echo "$dir",`echo $unique | tr '\n\r ' ',' `> attacksIssued.txt
	exit
done
