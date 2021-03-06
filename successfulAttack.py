#!/usr/bin/python

# Validates if a WIRED scenario's attack was successful during time of
# attack by reading mgen files.

import ast
import re
import sys
import shutil
import os

logPath =  os.getcwd()
flows = []
success = False
successString = ""
previousSecond = 0
lineBefore = ""
victim = ""
attacker = "";

if "spoofingAttack_sh" in logPath:
	parsedPath = logPath.split("spoofingAttack_sh")
	parsedAttacker = parsedPath[0].split("/")
	attacker = parsedAttacker[len(parsedAttacker)-1].split("_")[0]
	victim = parsedPath[1].split("_")[0]

else: #may be a blackhole attack
	parsedPath = logPath.split("blackholeAttack_sh")
	parsedAttacker = parsedPath[0].split("/")
	attacker = parsedAttacker[len(parsedAttacker)-1].split("_")[0]
	victim = (int(attacker)+5) # choose arbitrary victim to analyze
	if victim > 10:
		victim -= 10

attackerIPFlow = str(int(attacker) + 10) + ".0.0.2_"
mgenFile = str(int(victim) + 10) + "_0_0_2.mgencapture"

if "wireless" in logPath:
	attackerIPFlow = str(int(attacker) + 10) + ".0.0.2_"
	mgenFile =  "10_0_0_" + str(victim) + ".mgencapture"

# Function used to write success status of attack.
def writeToFile():
	successFile = open(logPath + "/success.txt", 'w')
	if success:
		successFile.write(logPath + " Attack succeeded: " + successString + "\n")
	else:
		successFile.write(" Attack failed: \n" + logPath + "\n")
		
	successFile.close()

attackSeenCount = 0

with open(logPath + "/" + mgenFile) as readFile:
	for line in readFile:

		lineCheck = line.split("}")

		# Avoid exception when line is short
		if len(lineCheck) > 2:
			
			# Split is used over and over to parse flows.
			columns = line.split(";")
			colAttributes = columns[1].split(":")
			
			if "none" not in line:
				attackSeenCount += 1
			
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
				if flow not in line and attackerIPFlow not in flow:
					success = True
					successString="Flow lost -> " + flow
					
					if "none" in line:
						success = False
			
			# Ignore ipv6 logs due to lack of parsing ability
			if "ipv6" in line or "ipv6" in lineBefore:
				success = False
				
			if success is True:
				writeToFile()
				sys.exit(0)
	
			previousSecond = time
			lineBefore = line

# Final condition checks if node completely dies and doesn't notice attack
if attackSeenCount < 10:
	success = True
	successString="Node dies during attack. " + str(attackSeenCount)

writeToFile()
