#!/bin/bash

#first count up for each node's file and store in all.results
for dir in `ls -d */`; do
	cd $dir
	echo "inside $dir"
	attackNum=`echo $dir | cut -d'_' -f1`
	echo "first char is " $attackNum 
	rm all.results
	file=n"$attackNum".capture
	echo "FILE",$file
	unique=`cat $file | cut -d';' -f6 | uniq`
	rm attacksIssued.txt
	echo `echo $unique | tr '\n\r ' ',' `> attacksIssued.txt

	for file in `ls *.capture | grep -v n"$attackNum".capture` ; do
	#	echo "working $file" "skipping"  n"$attackNum".capture
		len=`wc -l $file | cut -d' ' -f1`
		echo -n "$dir,$file," >> all.results
		cat $file | awk 'BEGIN { FS = ";" } ; { s+=$4;t+=$5 } END {print s","t}' >> all.results 
	done
	cd ../
done

#now count for each configuration the total
rm combined.results
for dir in `ls -d */`; do
	cd $dir
	echo -n "$dir," >> ../combined.results
	echo -n `cat all.results | awk 'BEGIN { FS = "," } ; { s+=$3;t+=$4 } END {print s","t}'` >> ../combined.results
	echo ","`cat attacksIssued.txt` >> ../combined.results
	
	cd ..
done
