#!/usr/bin/python
#Creates a file containing packet type sequences from an input field data file
import sys
from lxml import etree

numNodes = 10
scenName = '/root/IntelAttacker/staticScenarios/chainCoords.scen'
coordsFile = '/root/IntelAttacker/staticScenarios/cycleCoords.txt'


#Create the root element for the output file:
ScenarioXML = etree.Element("Scenario")

NetworkPlanXML = etree.SubElement(ScenarioXML, "NetworkPlan") 
###Configure the Network Plan
NetworkDefinitionXML = etree.SubElement(NetworkPlanXML, "NetworkDefinition", id=str(numNodes+1), name='wlan'+str(numNodes+1), type='WlanNode')
for i in range(1,numNodes+1):
	#each node's peer interface to the wlan device
	modelXML = etree.SubElement(NetworkDefinitionXML, "model", name='netem', netif='eth0', peer='n'+str(i))
	
	bwXML = etree.SubElement(modelXML, "bw")
	bwXML.text = '54000000'
	
	delayXML = etree.SubElement(modelXML, "delay")
	delayXML.text = '50000'
	
#wireless range
modelXML = etree.SubElement(NetworkDefinitionXML, "model", name='basic_range', type='wireless')

rangeXML = etree.SubElement(modelXML, "range")
rangeXML.text = '176'

bandwidthXML = etree.SubElement(modelXML, "bandwidth")
bandwidthXML.text = '54000000'

jitterXML = etree.SubElement(modelXML, "jitter")
jitterXML.text = '0'

delayXML = etree.SubElement(modelXML, "delay")
delayXML.text = '50000'

errorXML = etree.SubElement(modelXML, "error")
errorXML.text = '0'
	
#scenario mobility script

modelXML = etree.SubElement(NetworkDefinitionXML, "model", name='ns2script', type='mobility')

fileXML = etree.SubElement(modelXML, "file")
fileXML.text = scenName

refresh_msXML = etree.SubElement(modelXML, "refresh_ms")
refresh_msXML.text = '50'

loopXML = etree.SubElement(modelXML, "loop")
loopXML.text = '0'

autostartXML = etree.SubElement(modelXML, "autostart")
autostartXML.text = '1.0'

mapXML = etree.SubElement(modelXML, "map")

script_startXML = etree.SubElement(modelXML, "script_start")

script_pauseXML = etree.SubElement(modelXML, "script_pause")

script_stopXML = etree.SubElement(modelXML, "script_stop")

#Network Plan's Nodes
for i in range(1,numNodes+1):
	NodeXML = etree.SubElement(NetworkPlanXML, "Node", id=str(i), name='n'+str(i), type='router')
	
	interfaceXML = etree.SubElement(NodeXML, "interface", name='eth0', net='wlan'+str(numNodes+1))
	
	addressXML = etree.SubElement(interfaceXML, "address", type='mac')
	addressXML.text = '00:00:00:aa:00:'+str(i)

	addressXML = etree.SubElement(interfaceXML, "address")
	addressXML.text = '10.0.0.'+str(i)+'/32'
	
	addressXML = etree.SubElement(interfaceXML, "address")
	addressXML.text = 'a::'+str(i)+'/128'

########### End of NetworkPlan#########

########### Configure MotionPlan######
MotionPlanXML = etree.SubElement(ScenarioXML, "MotionPlan") 
originXML = etree.SubElement(MotionPlanXML, "origin", alt='2.0', lat='47.5791667', lon='-122.132322', scale100='150.0')

NodeXML = etree.SubElement(MotionPlanXML, "Node", name='wlan'+str(numNodes+1))
motionXML = etree.SubElement(NodeXML, "motion", type='stationary')
pointXML = etree.SubElement(motionXML, "point")
pointXML.text = '0,0'

#read the "scenario".txt coordinate file for the rest of the node configurations
coordLines = open(coordsFile)
for i in range(1,numNodes+1):
	NodeXML = etree.SubElement(MotionPlanXML, "Node", name='n'+str(i))
	motionXML = etree.SubElement(NodeXML, "motion", type='stationary')
	pointXML = etree.SubElement(motionXML, "point")
	pointXML.text = coordLines.readline().replace(' ',',')

########### End of MotionPlan#########

########### Configure ServicePlan######
ServicePlanXML = etree.SubElement(ScenarioXML, "ServicePlan") 
NodeXML = etree.SubElement(ServicePlanXML, "Node", type='router')
ServiceXML = etree.SubElement(NodeXML, "Service", name='zebra')
ServiceXML = etree.SubElement(NodeXML, "Service", name='OSPFv2')
ServiceXML = etree.SubElement(NodeXML, "Service", name='OSPFv3')
ServiceXML = etree.SubElement(NodeXML, "Service", name='vtysh')
ServiceXML = etree.SubElement(NodeXML, "Service", name='IPForward')

for i in range(1,numNodes+1):
	NodeXML = etree.SubElement(ServicePlanXML, "Node", name='n'+str(i))
	ServiceXML = etree.SubElement(NodeXML, "Service", name='OLSR', startup_idx='45')
	ServiceXML = etree.SubElement(NodeXML, "Service", name='IPForward', startup_idx='5')
	ServiceXML = etree.SubElement(NodeXML, "Service", custom='True', name='UserDefined', startup_idx='35')
	FileXML = etree.SubElement(ServiceXML, "File", name='custom-post-config-commands.sh')
	FileXML.text = '''
route add default dev eth0
route add -net 224.0.0.0 netmask 224.0.0.0 dev eth0
    
#!/bin/sh
HN=`hostname`
if [ `uname` = &quot;FreeBSD&quot; ]; then
  SCRIPTDIR=/tmp/e0_$HN
else SCRIPTDIR=/root/
fi
cd $SCRIPTDIR
mkdir 1_60_60_downAttack_sh_chainCoords_scen_OLSR_chainCoords_txt
cd 1_60_60_downAttack_sh_chainCoords_scen_OLSR_chainCoords_txt
    
#get ip of current
hostnameLen=`expr length $HN`
hostnameLen=`expr $hostnameLen - 1`
myIP=&quot;10.0.0.`expr substr $HN 2 $hostnameLen`&quot;

#now insert attack script
if [ `hostname` = n1 -o 1 = 0 ]
then

#start logging
tshark -nli eth0 -T fields -E separator=, -e frame.time_epoch -e frame.len -e frame.protocols -e ip.src -e ip.dst -e ipv6.src -e ipv6.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport | /root/IntelAttacker/netCollect.py $myIP &gt; $HN.capture &amp;    

mgen flush input /root/IntelAttacker/flowGenerator/flows/flow`hostname`.mgn output /dev/null &amp;

(
cat &lt;&lt; 'EOF'
#!/bin/bash

startTime=$1
duration=$2

echo &quot;none&quot; &gt; /tmp/attack.txt
sleep $startTime
echo &quot;down&quot; &gt; /tmp/attack.txt
ifconfig eth0 down
sleep $duration

ifconfig eth0 up
rm /tmp/attack.txt

EOF
) &gt; attack.sh

chmod 755 attack.sh

./attack.sh 60 60  
else
echo `hostname` &gt;&gt; /tmp/check.txt
mgen flush input /root/IntelAttacker/flowGenerator/flows/flow`hostname`.mgn | /root/IntelAttacker/mgenCollect.py &gt; `hostname`.mgencapture &amp;
fi
'''
	CommandXML = etree.SubElement(ServiceXML, "Command", type='start')
	CommandXML.text = 'sh custom-post-config-commands.sh'
CoreMetaDataXML = etree.SubElement(ScenarioXML, "CoreMetaData") 

MetaDataXML = etree.SubElement(CoreMetaDataXML, "MetaData") 

paramXML = etree.SubElement(MetaDataXML, "param", name='global_options') 
paramXML.text = 'interface_names=no ip_addresses=yes ipv6_addresses=yes node_labels=yes link_labels=yes show_api=no background_images=no annotations=yes grid=no traffic_start=0'

paramXML = etree.SubElement(MetaDataXML, "param", name='canvas c1') 
paramXML.text = '{name {Canvas1}} {wallpaper-style {upperleft}} {wallpaper {sample4-bg.jpg}} {size {1000 750}}'

#output the xml tree	
print etree.tostring(ScenarioXML,pretty_print='true')
