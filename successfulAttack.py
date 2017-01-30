#!/usr/bin/python

# Validates if a WIRED scenario's attack was successful 
# by reading mgen files.

import ast
import re
import sys
import shutil

logPath = sys.argv[1]
flows = []
success = False
successString=""
previousSecond = 0
lineBefore=""

parsedPath = logPath.split("spoofingAttack_sh")
victim = parsedPath[1].split("_")[0]
mgenFile = "n" + victim + ".mgencapture"
print victim


# Function used to write success status of attack.
def writeToFile():
	successFile = open(logPath + "/success.txt", 'w')
	if success:
		successFile.write("Attack succeeded: " + successString + "\n")
	else:
		successFile.write("Attack failed: \n" + logPath + "\n")
		
	successFile.close()


with open(logPath + "/" + mgenFile) as readFile:
	for line in readFile:
		# Split is used over and over to parse flows.
		columns = line.split(";")
		colAttributes = columns[1].split(":")
		
		for values in colAttributes: 
			toBeCleaned = values.split("'")
			
			for possibleFlow in toBeCleaned: 
				if "_" in possibleFlow and possibleFlow not in flows:
					flows.append(possibleFlow)
		
		time = int(ast.literal_eval(columns[0]))
		timeDiff = time - previousSecond
		
		# Conditions check if time between events was too great or if flow is missing. 
		if timeDiff > 5:
			success = True
			successString="Time greater than 5 seconds lost."
			
		for flow in flows:
			if flow not in line:
				success = True
				successString="Flow lost -> " + flow
		
		# Ignore ipv6 logs due to lack of parsing ability
		if "ipv6" in line or "ipv6" in lineBefore:
			success = False
			
		if success is True:
			writeToFile()
			sys.exit(0)

		previousSecond = time
		lineBefore = line
writeToFile()
