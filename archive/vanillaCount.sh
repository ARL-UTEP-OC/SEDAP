#!/bin/bash

#get all counts without 1 node
for dir in "vanilla1/" "vanilla2/"
do
	cd $dir
	for ignoreNode in {1..10}
	do
		file=n"$ignoreNode".capture
		allButFile=`ls *.capture | grep -v n"$ignoreNode".capture`
		echo "working $file" "skipping"  n"$ignoreNode".capture
		rm all.results.n$ignoreNode
		len=`wc -l $file | cut -d' ' -f1`
		echo -n "$dir,$file," >> all.results.n$ignoreNode
		cat $allButFile | awk 'BEGIN { FS = ";" } ; { s+=$4;t+=$5 } END {print s","t}' >> all.results.n$ignoreNode
	done
	cd ../
done

#now count for each configuration the total
rm combinedVanilla.results
for dir in "vanilla1/" "vanilla2"
do
	cd $dir
	for ignoreNode in {1..10}
		do
		echo -n "$dir"_n"$ignoreNode", >> ../combinedVanilla.results
		echo `cat all.results.n$ignoreNode | awk 'BEGIN { FS = "," } ; { s+=$3;t+=$4 } END {print s","t}'` >> ../combinedVanilla.results
		
	done
	cd ..
done
