#!/bin/bash

cd -v /root/

for dir in `ls -d *_txt`; do
        
	newname=`echo $dir | sed -e 's/\'__'/'_'/g'`
       
        if [ "$dir" != "$newname" ]
        then
 		mv $dir $newname
	fi
done
