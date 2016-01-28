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


def insertAttack():
	global myStr 
	myStr+="""
    custom-post-config-commands {
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
    }"""
	if "OSPF" in routingProtocol or "RIP" in routingProtocol:
		serviceString += " zebra vtysh "
	myStr+="""
    services {"""+str(serviceString) + """ IPForward}
    """

#Read file and get 1 line at a time here
coordLines = open("/root/IntelAttacker/staticScenarios/"+coordFile)
myStr = ""
for i in range(1,numNodes+1):
    myStr += """
node n"""+str(i)+""" {
    type router
    """
    if "RIP" or "OLSR" in routingProtocol:
        myStr += "model router"
    else: myStr += "model mdr"
    myStr += """
    network-config {
	hostname n"""+str(i)+"""
	!
	interface eth0
	 ip address 10.0.0."""+str(i)+"""/32
	 ipv6 address a:0::"""+str(i)+"""/128
	!
    }
    iconcoords {"""+coordLines.readline()+"""}
    labelcoords {196.387421 486.134022}
    canvas c1
    interface-peer {eth0 n"""+str(numNodes+1)+"""}
"""
    insertAttack()
    myStr +="""
}
"""
#############
myStr += """
node n"""+str(numNodes+1)+""" {
    type wlan
    network-config {
	hostname wlan"""+str(numNodes+1)+"""
	!
	interface wireless
	 ip address 10.0.1.0/24
	 ipv6 address a:1::0/64
	!
	scriptfile
	/root/IntelAttacker/staticScenarios/"""+mobility+"""
	!
	mobmodel
	coreapi
	basic_range
	ns2script
	!
    }
    iconcoords {0 0}
    labelcoords {0 0}
    canvas c1"""
for i in range(0,numNodes):
    myStr += """
    interface-peer {e"""+str(i)+""" n"""+str(i+1)+"""}"""
myStr +="""
	custom-config {
	custom-config-id basic_range
	custom-command {3 3 9 9 9}
	config {
	range=176
	bandwidth=54000000
	jitter=0
	delay=50000
	error=0
	}
    }
    custom-config {
	custom-config-id ns2script
	custom-command {10 3 11 10 10 10 10 10}
	config {
	file=/root/IntelAttacker/staticScenarios/"""+mobility+"""
	refresh_ms=50
	loop=0
	autostart=1.0
	map=
	script_start=
	script_pause=
	script_stop=
	}
    }
}
"""

for i in range(1,numNodes+1):
    myStr += """
link l"""+str(i)+""" {
    nodes {n"""+str(numNodes+1)+""" n"""+str(i)+"""}
    bandwidth 54000000
    delay 50000
}
"""
myStr += """
canvas c1 {
    name {Canvas1}
    wallpaper-style {upperleft}
    wallpaper {sample4-bg.jpg}
    size {1000 750}
}


option global {
    interface_names no
    ip_addresses yes
    ipv6_addresses yes
    node_labels yes
    link_labels yes
    ipsec_configs yes
    remote_exec no
    exec_errors yes
    show_api no
    background_images no
    annotations yes
    grid no
}
"""
print myStr
