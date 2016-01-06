#!/usr/bin/python
#Creates a file containing packet type sequences from an input field data file
import sys
from lxml import etree

numNodes = 10
scenName = '/root/IntelAttacker/staticScenarios/chainCoords.scen'


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
modelXML = etree.SubElement(NetworkDefinitionXML, "model", name='basic_Range', type='wireless')

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

###########
MotionPlanXML = etree.SubElement(ScenarioXML, "MotionPlan") 
ServicePlanXML = etree.SubElement(ScenarioXML, "ServicePlan") 
CoreMetaDataXML = etree.SubElement(ScenarioXML, "CoreMetaData") 

#output the xml tree	
print etree.tostring(ScenarioXML,pretty_print='true')
