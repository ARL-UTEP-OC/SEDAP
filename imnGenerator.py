#!/usr/bin/python

# Generates .imn files based on parameters passed in.
# Currently capable of generating wired and wireless .imns

import sys
import os
import commands

startTime = sys.argv[1]
duration = sys.argv[2]
numNodes = int(sys.argv[3])
attackNodeNumber = sys.argv[4]
attackScriptPath = sys.argv[5]
scenario = sys.argv[6]
routingProtocol= sys.argv[7]
wireTypeDir = sys.argv[8]

workingDirectory = os.getcwd()
rootDirectory = "/root/" + wireTypeDir + "/"
spoofNode = ""
wired="wired" in wireTypeDir
attackScriptInputs = []

#the script path contains inputs for the string separated by '.'
attackScriptPathInputsSplit = attackScriptPath.split("spoofingAttack.sh")
if len(attackScriptPathInputsSplit) > 1:
    attackScriptPath = "spoofingAttack.sh"
    attackScriptInputs.append(attackScriptPathInputsSplit[1])
    spoofNode = attackScriptPathInputsSplit[1]

elif attackScriptPath == "blackholeAttack.sh":
    attackScriptInputs.append(attackNodeNumber)
    attackScriptInputs.append(str(numNodes))

maxNodes = int(numNodes)
if wired:
	maxNodes = int(numNodes) * 2

def insertBasicConfigs():
	global myStr
	
	myStr += """
	custom-config-id service:UserDefined:custom-post-config-commands.sh
	custom-command custom-post-config-commands.sh
	config {"""
	
	if not wired:
		myStr += """
route add default dev eth0
route add -net 224.0.0.0 netmask 224.0.0.0 dev eth0"""

	myStr += """
#!/bin/sh
HN=`hostname`
if [ `uname` = "FreeBSD" ]; then
  SCRIPTDIR=/tmp/e0_$HN
else SCRIPTDIR=""" + rootDirectory + """
fi
cd $SCRIPTDIR
"""

def insertMgen():
	global myStr
	
	logPath = attackNodeNumber+"_"+startTime+"_"+duration+"_"+attackScriptPath+spoofNode
	logPath+="_"+scenario+"_"+routingProtocol+"_"+wireTypeDir
	logPath = logPath.replace(".","_")
	logPath = logPath.replace("/","_")
	logPath += "*"
	
	myStr += """
mkdir """ + logPath + """
cd """ + logPath +"""

#get ip of current
hostnameLen=`expr length $HN`
hostnameLen=`expr $hostnameLen - 1` """
	if wired:
		myStr += """
myIP="`expr substr $HN 2 $hostnameLen`.0.0.1" 
"""

		if "OSPF" in routingProtocol and nodeCount == int(attackNodeNumber):
			myStr += """
#stop quagga
#killall vtysh
#killall ospfd
#killall zebra
"""

	else:
		myStr += """
myIP="10.0.0.`expr substr $HN 2 $hostnameLen`" 
"""

	myStr += """
#now insert attack script and mgen flush if node is attacker
if [ `hostname` = n""" + attackNodeNumber + """ -o """ + attackNodeNumber + """ = 0 ]
then

#start logging
tshark -a duration:175 -nli eth0 -T fields -E separator=, -e frame.time_epoch -e frame.len -e frame.protocols -e ip.src -e ip.dst -e ipv6.src -e ipv6.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport | """ + workingDirectory + """/netCollect.py """ + rootDirectory + logPath + """ $myIP > $HN.capture &    

mgen flush input """ + workingDirectory + """/flowGenerator/flows/flow`hostname`.mgn output /dev/null &

(
cat << 'EOF'
"""
	myStr += commands.getoutput("cat " +str("wireTypeAttacks/" + wireTypeDir + "Attacks/" + attackScriptPath)) + """
EOF
) > attack.sh

chmod 755 attack.sh

./attack.sh """ + startTime + " " + duration
	for attackScriptInput in attackScriptInputs:
		myStr+=" "+attackScriptInput
	myStr+=" " + rootDirectory + logPath + """ 

else
	echo `hostname` >> """ + rootDirectory + logPath +"""/check.txt
	mgen flush input """ + workingDirectory + """/flowGenerator/flows/flow`hostname`.mgn | """ + workingDirectory + """/mgenCollect.py """ + rootDirectory + logPath + """ > `hostname`.mgencapture &
fi
"""

def insertRoutingProtocol(router):
	global myStr
	
	if router is True:
		
		serviceString = routingProtocol
		
		if "OLSR" in routingProtocol:
			serviceString += "_Mod IPForward"
			
		else:
			serviceString += " zebra vtysh IPForward"
	else:
		serviceString = "DefaultRoute SSH"
	
	myStr+="""
	services {"""+str(serviceString) + """ UserDefined}
"""

myStr = ""
nodeCount = 0
scenarioFile="staticScenarios/" + wireTypeDir + "_scenarios/" + scenario + ".imn"

with open(scenarioFile) as readFile:

	readyToInsert = False
	
	for line in readFile:
		
		nodeIsAttacker = nodeCount == int(attackNodeNumber)
		inRange = nodeCount <= int(numNodes)
		
		if readyToInsert is True:
			insertBasicConfigs()
			
			# Inserts configurations for everything but wlan11
			if inRange:
				insertMgen()
				
			myStr += """
	}
	}
    custom-config {
	custom-config-id service:UserDefined
	custom-command UserDefined
	config {
	files=('custom-post-config-commands.sh', )
	startidx=120
	cmdup=('sh custom-post-config-commands.sh', )
	}
    }
"""			# Will only insert routing protocols for routers.
			isRouter = True
			
			if not wired and inRange:
				insertRoutingProtocol(isRouter)

			elif wired:
				if not inRange or nodeIsAttacker:
					insertRoutingProtocol(isRouter)
				else:
					isRouter = False
					insertRoutingProtocol(isRouter)
				
			readyToInsert = False

		
		if "model host" in line and nodeIsAttacker:
			myStr += """
	model router"""
			continue
		
		elif "node n" in line:
			nodeCount += 1
			
		elif "custom-config {" in line and nodeCount <= maxNodes:
			readyToInsert = True
		
		myStr += line

print myStr
