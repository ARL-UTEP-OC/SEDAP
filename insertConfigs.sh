#!/bin/bash

#This script is responsible for inserting text passed within it based on 
#the string to be found, the string so place after the finding, and the 
#occurance to find (ex. node 1 or node 15).

toFind=$(echo "$1" | sed -e 's/[&]/\\&/g') #sed to escape special chars.
#must make explicit declaration of string when being called from python
replace=$(printf '%q' "$2")
replaceWith=$(echo "$replace" | sed -e 's/[&]/\\&/g') #sed to escape special chars.
occurence=$3
filePath=$4

if [[ $toFind ==  *"model host"* ]]
then
	#to replace existing string at particular occurence
	sed -i ':a;N;$!ba;s/\n/\x0/g;s/'"$toFind"'/'"$replaceWith"'/'"$occurence"';s/\x0/\n/g' $filePath
elif [[ $toFind ==  *"------"* ]]
then
	#delete all occurences
	sed -i '/'$toFind'/d' $filePath
else
	#to append to existing string
	sed -i ':a;$!{N;ba};s@\('"$toFind"'\)@\1\n'"$replaceWith"'@'"$occurence"'' "$filePath"
fi

	
#to replace all occurences
#sed "/$toFind/a $replaceWith" $filePath

	
