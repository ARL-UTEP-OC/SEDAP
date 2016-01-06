#!/usr/bin/python

import sys
import commands

#get command line args:
startTime = sys.argv[1]
duration = sys.argv[2]
numNodes = int(sys.argv[3])
attackNodeNumber = sys.argv[4]
attackScriptPath = sys.argv[5]
attackScriptInputs = []
#the script path contains inputs for the string separated by '.'
attackScriptPathInputsSplit = attackScriptPath.split("spoofingAttack.sh")
if len(attackScriptPathInputsSplit) > 1:
    attackScriptPath = "spoofingAttack.sh"
    attackScriptInputs.append(attackScriptPathInputsSplit[1])

if attackScriptPath == "blackholeAttack.sh":
    attackScriptInputs.append(attackNodeNumber)
    attackScriptInputs.append(str(numNodes))       

mobility = sys.argv[6]
routingProtocol= sys.argv[7]
coordFile = sys.argv[8]




##############The attack script import##########
'''
route add default dev eth0
route add -net 224.0.0.0 netmask 224.0.0.0 dev eth0
    """
	myStr += """
#!/bin/sh
HN=`hostname`
if [ `uname` = "FreeBSD" ]; then
  SCRIPTDIR=/tmp/e0_$HN
else SCRIPTDIR=/root/
fi
cd $SCRIPTDIR
"""
	logPath = attackNodeNumber+"_"+startTime+"_"+duration+"_"+attackScriptPath
	for attackScriptInput in attackScriptInputs:
		logPath+="_"+attackScriptInput
	logPath+="_"+mobility+"_"+routingProtocol+"_"+coordFile
	logPath = logPath.replace(".","_")
	logPath = logPath.replace("/","_")
	myStr += "mkdir " + logPath + """
cd """ + logPath +"""
    
#get ip of current
hostnameLen=`expr length $HN`
hostnameLen=`expr $hostnameLen - 1`
myIP="10.0.0.`expr substr $HN 2 $hostnameLen`"

#now insert attack script
if [ `hostname` = n"""+attackNodeNumber+""" -o """ + attackNodeNumber + """ = 0 ]
then

#start logging
tshark -nli eth0 -T fields -E separator=, -e frame.time_epoch -e frame.len -e frame.protocols -e ip.src -e ip.dst -e ipv6.src -e ipv6.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport | /root/IntelAttacker/netCollect.py $myIP > $HN.capture &    

mgen flush input /root/IntelAttacker/flowGenerator/flows/flow`hostname`.mgn output /dev/null &

(
cat << 'EOF'
"""
	myStr += commands.getoutput("cat " +str(attackScriptPath)) + """
EOF
) > attack.sh

chmod 755 attack.sh

./attack.sh """ + startTime +" " + duration + " "
	for attackScriptInput in attackScriptInputs:
		myStr+=" "+attackScriptInput
	myStr+=" " 
	serviceString = routingProtocol

	myStr+="""
else
	echo `hostname` >> /tmp/check.txt
	mgen flush input /root/IntelAttacker/flowGenerator/flows/flow`hostname`.mgn | /root/IntelAttacker/mgenCollect.py > `hostname`.mgencapture &
fi
'''
