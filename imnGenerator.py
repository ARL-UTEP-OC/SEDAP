#!/usr/bin/python

# Generates .imn configurations to be passed in based on parameters given.
# Currently capable of generating wired and wireless .imns

import sys
import os
import commands
import subprocess

startTime = sys.argv[1]
duration = sys.argv[2]
numNodes = int(sys.argv[3])
attackNodeNumber = sys.argv[4]
attackScriptPath = sys.argv[5]
scenario = sys.argv[6]
routingProtocol= sys.argv[7]
wireTypeDir = sys.argv[8]
path = sys.argv[9]
subnet = sys.argv[10]

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
	
	basicConfigs = """------
	custom-config-id service:UserDefined:custom-post-config-commands.sh
	custom-command custom-post-config-commands.sh
	config {"""
	
	if not wired:
		basicConfigs += """
route add default dev eth0
route add -net 224.0.0.0 netmask 224.0.0.0 dev eth0"""

	basicConfigs += """
#!/bin/sh
HN=`hostname`
if [ `uname` = "FreeBSD" ]; then
  SCRIPTDIR=/tmp/e0_$HN
else SCRIPTDIR=""" + rootDirectory + """
fi
cd $SCRIPTDIR

	}
	}
    custom-config {
	custom-config-id service:UserDefined
	custom-command UserDefined
	config {
	files=('custom-post-config-commands.sh', )
	startidx=120
	cmdup=('sh custom-post-config-commands.sh', )
------"""
	return basicConfigs

def insertMgen(node):

	logPath = attackNodeNumber+"_"+startTime+"_"+duration+"_"+attackScriptPath+spoofNode
	logPath+="_"+scenario+"_"+routingProtocol+"_"+wireTypeDir+"_"+subnet
	logPath = logPath.replace(".","_")
	logPath = logPath.replace("/","_")
	
	mgenConfigs = """------
mkdir """ + logPath + """
cd """ + logPath +"""

#get ip of current
hostnameLen=`expr length $HN`
hostnameLen=`expr $hostnameLen - 1` """
	if wired:
		mgenConfigs += """
myIP="`expr substr $HN 2 $hostnameLen`.0.0.1" 
"""
	else:
		mgenConfigs += """
myIP="10.0.0.`expr substr $HN 2 $hostnameLen`" 
"""

	mgenConfigs += """
#now insert attack script and mgen flush if node is attacker
if [ `hostname` = n""" + attackNodeNumber + """ -o """ + attackNodeNumber + """ = 0 ]
then

#start logging
tshark -a duration:175 -nli eth0 -T fields -E separator=, -e frame.time_epoch -e frame.len -e frame.protocols -e ip.src -e ip.dst -e ipv6.src -e ipv6.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport | """ + workingDirectory + """/netCollect.py """ + rootDirectory + logPath + """ $myIP > $HN.capture &    

mgen flush input """ + workingDirectory + """/flowGenerator/flows/flow`hostname`.mgn output /dev/null &

(
cat << 'EOF'
"""
	mgenConfigs += commands.getoutput("cat " +str("wireTypeAttacks/" + wireTypeDir + "Attacks/" + attackScriptPath)) + """
EOF
) > attack.sh

chmod 755 attack.sh

./attack.sh """ + startTime + " " + duration
	for attackScriptInput in attackScriptInputs:
		mgenConfigs+=" "+attackScriptInput
	mgenConfigs+=" " + rootDirectory + logPath + """ 

else
	echo `hostname` >> """ + rootDirectory + logPath +"""/check.txt
	mgen flush input """ + workingDirectory + """/flowGenerator/flows/flow`hostname`.mgn | """ + workingDirectory + """/mgenCollect.py """ + rootDirectory + logPath + """ > `hostname`.mgencapture &
fi
------"""
	return mgenConfigs

def insertRoutingProtocol(router):
	
	if router is True:
		
		serviceString = routingProtocol
		
		if "OLSR" in routingProtocol:
			serviceString += " IPForward"
			
		else:
			serviceString += " zebra vtysh IPForward"
	else:
		serviceString = "DefaultRoute SSH"
	
	service ="""------
    }
    }
	services {"""+str(serviceString) + """ UserDefined
------"""
	return service

scenarioFile="staticScenarios/" + wireTypeDir + "_scenarios/" + scenario + ".imn"
basicConfigs = insertBasicConfigs()

toFindConfig = """custom-config {"""
toFindBasic = """cd $SCRIPTDIR"""
toFindService = """cmdup=('sh custom-post-config-commands.sh', )"""

for node in range(1,maxNodes+1):
	
	nodeIsAttacker = node == int(attackNodeNumber)
	inRange = node <= int(numNodes)

	adjustedConfigValue = int(node)*2 - 1
	subprocess.call(["./insertConfigs.sh", toFindConfig, basicConfigs, str(adjustedConfigValue), path])

	# Inserts configurations for everything but wlan11
	if inRange:
		mgenConfigs = insertMgen(node)
		subprocess.call(["./insertConfigs.sh", toFindBasic, mgenConfigs, str(node), path])

		
	if not wired and inRange:
		services = insertRoutingProtocol(True)


	# Will insert services based on router or host
	isRouter = True
		
	if not wired and inRange:
		isRouter = True

	elif wired:
		if not inRange or nodeIsAttacker:
			isRouter = True
		else:
			isRouter = False

	services = insertRoutingProtocol(isRouter)
	subprocess.call(["./insertConfigs.sh", toFindService, services, str(node), path])


toFindModel="""model host"""
replaceModel="""model router"""

subprocess.call(["./insertConfigs.sh", toFindModel, replaceModel, attackNodeNumber, path])

subprocess.call(["./insertConfigs.sh", """------""", "", "0", path])
