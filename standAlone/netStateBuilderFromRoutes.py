#!/usr/bin/python
import sys
import networkx as nx
import xml.etree.ElementTree as ET
from lxml import etree
from netaddr import *
import logging

instance = ""

#globals
gateways = {} #(src, dest) -> (gateway, metric)
directLinks = {} #(src, dest) -> ('0.0.0.0', metric)
G = nx.Graph()
nodes = {} 

attackName = ""
victim = None
attackNode = None
flows = [] #(src, dest, type)

#Create the root element for the output file:
attributesXML = etree.Element("Attributes")

#parameters for output
flowDescriptionAttributes = {}
flowDescriptionAttributes["fromHop"]=''
flowDescriptionAttributes["toHop"]=''
flowDescriptionAttributes["typeName"]=''
flowDescriptionAttributes["distance"]=''
flowDescriptionAttributes["passthrough"]=''
flowDescriptionAttributes["srcSpoofed"]=''
flowDescriptionAttributes["destSpoofed"]=''
flowDescriptionAttributes["hopsToSpoofed"]=''
flowDescriptionAttributes["hopsFromSpoofedToDest"]=''
flowDescriptionAttributes["spoofedBetweenAttacker"]=''
flowDescriptionAttributes["isDstBetweenSpoofedAndAttacker"]=''
flowDescriptionAttributes["spoofedBetweenAttackergw"]=''
flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]=''
flowDescriptionAttributes["isAttackerBetweenSpoofedAndDst"]=''
flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]=''
flowDescriptionAttributes["isSrcBetweenSpoofedAndDst"]=''
flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]=''
flowDescriptionAttributes["altPathWithoutAttacker"]=''


def extractLinksfromRoutes(nodeIP, routes):
	global gateways
	global G

	#initialize the elements string
	elements = ""
	#remove extra spaces:
	for line in routes.split('\n'):
		line = ' '.join(line.split())
		elements = line.split(" ")
		#ignore if the destination subnet is 0.0.0.0 or multicast 224...
		if elements[0] == '0.0.0.0' or elements [0].startswith('224.'):
			continue
		#otherwise, if 2nd column is 0.0.0.0, then this is a direct link
		dest = elements[0] + "/" + elements[2]
		if elements[1] == '0.0.0.0':
			directLinks[(nodeIP,IPNetwork(dest))] = (elements[1], elements[4])
			#also add direct links to our networkx graph for later processing
			G.add_edge(nodeIP,IPNetwork(dest))
		#otherwise, this we extract the gateway
		else:
			gateways[(nodeIP,IPNetwork(dest))] = (elements[1], elements[4])

def getPathThroughGW(src, dst):
	path = []
	curr = ()
	if (src, dst) in directLinks:
		path.append(dst)
		return path
	if (src, dst) not in gateways:
		return None
	#get next hop
	curr = gateways[(src,dst)]
	while curr != None:
		#need to do the following lookup to re-obtain the netmask for the current IP address
		#convert string to IPAddress
		curr = IPAddress(curr[0])
		#now get entry with netmask
		if curr not in nodes:
			#somethings wrong...
			print curr,"not found in nodes list!"
			curr = None
			return None
		curr = nodes[curr]
		path.append(curr)
		if (curr,dst) in directLinks:
			curr = directLinks[(curr,dst)]
			#found a direct link so we're done
			path.append(dst)
			curr = None
		elif (curr, dst) in gateways:
			curr = gateways[(curr,dst)]
		else:
			print curr,"no path found!"
			curr = None
			return None			
	return path

def getSubPath(param1, param2):
	answer = []
	#check if param1 is a subpath of param2
	if len(param1) > len(param2):
		return []
	for i in range(0,len(param1)):
		if param1[i] == param2[i]:
			answer.append(param1[i])
		else:
			return answer
	return answer
	

def generateParametersFromTrafficProfile():
	global flows
	global flowDescriptionAttributes
	global flowDescriptionAttributesXML
	
	for flow in flows:
		#flowDescriptionAttributes["fromHop"]
		src = flow[0]
		dst = flow[1]
		
		logging.debug( "looking for: %s",(attackNode,src))
		if ((attackNode,src)) in directLinks:
			flowDescriptionAttributes["fromHop"] = directLinks[(attackNode,src)][1]
		elif ((attackNode,src)) in gateways:
			flowDescriptionAttributes["fromHop"] = gateways[(attackNode,src)][1]
		else:
			print flowDescriptionAttributes["fromHop"],"not found"
			exit
		logging.debug("fromHop %s",flowDescriptionAttributes["fromHop"])

		#flowDescriptionAttributes["toHop"]
		logging.debug("looking for: %s",(attackNode,dst))
		if ((attackNode,dst)) in directLinks:
			flowDescriptionAttributes["toHop"] = directLinks[(attackNode,dst)][1]
		elif ((attackNode,dst)) in gateways:
			flowDescriptionAttributes["toHop"] = gateways[(attackNode,dst)][1]
		else:
			print flowDescriptionAttributes["toHop"],"not found"
			exit
		logging.debug("toHop %s",flowDescriptionAttributes["toHop"])
		
		#type
		typeName = flow[2]
		if typeName.startswith("'") == False:
			typeName = "'"+flow[2]
		if typeName.endswith("'") == False:
			typeName = typeName+"'"
		flowDescriptionAttributes["typeName"] = typeName
		logging.debug("type %s",flowDescriptionAttributes["typeName"])
		
		#flowDescriptionAttributes["distance"]
		logging.debug("looking for:  %s",(src,dst))
		if ((src,dst)) in directLinks:
			flowDescriptionAttributes["distance"] = directLinks[(flow[0],dst)][1]
		elif ((src,dst)) in gateways:
			flowDescriptionAttributes["distance"] = gateways[(src,dst)][1]
		else:
			print flowDescriptionAttributes["distance"],"not found"
			exit
		logging.debug("distance %s",flowDescriptionAttributes["distance"])
		###path function test
		logging.debug("looking for path:  %s",(src,dst))
		logging.debug("\nPath\n %s",getPathThroughGW(src, dst))
		###
		
		logging.debug("\npassthrough check:  %s  in %s",attackNode, (src,dst))
		if attackNode in getPathThroughGW(src,dst):
			flowDescriptionAttributes["passthrough"]="True"
		else:
			flowDescriptionAttributes["passthrough"]="False"
########The following parameters are only valid if attack is spoofing#####
		logging.debug("\nsrc spoofed:  %s %s",src, victim)
		if src == victim:
			flowDescriptionAttributes["srcSpoofed"]="True"
		else:
			flowDescriptionAttributes["srcSpoofed"]="False"
		logging.debug("srcSpoofed %s",flowDescriptionAttributes["srcSpoofed"])

		logging.debug("\ndst spoofed:  %s %s",dst, victim)
		if dst == victim:
			flowDescriptionAttributes["destSpoofed"]="True"
		else:
			flowDescriptionAttributes["destSpoofed"]="False"
		logging.debug("destSpoofed %s",flowDescriptionAttributes["destSpoofed"])

		logging.debug("checking hopsToSpoofed from: %s to %s",attackNode,victim)
		if (attackNode,victim) in directLinks:
			flowDescriptionAttributes["hopsToSpoofed"]=directLinks[(attackNode,victim)][1]
		elif (attackNode,victim) in gateways:
			flowDescriptionAttributes["hopsToSpoofed"]=gateways[(attackNode,victim)][1]
		else: 
			flowDescriptionAttributes["hopsToSpoofed"]='-1'
		logging.debug("hopsToSpoofed %s",flowDescriptionAttributes["hopsToSpoofed"])
			
		logging.debug("checking hopsFromSpoofedToDest from: %s to %s",victim,dst)
		if (victim,dst) in directLinks:
			flowDescriptionAttributes["hopsFromSpoofedToDest"]=directLinks[(victim,dst)][1]
		elif (victim,dst) in gateways:
			flowDescriptionAttributes["hopsFromSpoofedToDest"]=gateways[(victim,dst)][1]
		else: 
			flowDescriptionAttributes["hopsFromSpoofedToDest"]='-1'
		logging.debug("hopsFromSpoofedToDest %s",flowDescriptionAttributes["hopsFromSpoofedToDest"]	)
		
		logging.debug("checking spoofedBetweenAttacker. Is: %s between (or equal to either) %s to %s",victim,src,attackNode)
		if victim == src:
			flowDescriptionAttributes["spoofedBetweenAttacker"]="True"
		elif victim in getPathThroughGW(src,attackNode):
			flowDescriptionAttributes["spoofedBetweenAttacker"]="True"
		else:
			flowDescriptionAttributes["spoofedBetweenAttacker"]="False"
		logging.debug("spoofedBetweenAttacker %s",flowDescriptionAttributes["spoofedBetweenAttacker"])
		
		logging.debug("checking isDstBetweenSpoofedAndAttacker. Is: %s between (or equal to either) %s to %s",dst,victim,attackNode)
		if dst == victim:
			flowDescriptionAttributes["isDstBetweenSpoofedAndAttacker"]="True"
		elif dst in getPathThroughGW(victim,attackNode):
			flowDescriptionAttributes["isDstBetweenSpoofedAndAttacker"]="True"
		else:
			flowDescriptionAttributes["isDstBetweenSpoofedAndAttacker"]="False"
		logging.debug("isDstBetweenSpoofedAndAttacker %s",flowDescriptionAttributes["isDstBetweenSpoofedAndAttacker"])
		
#######
		#algorithm used to check: if path(src,dst) startswith(path(src,att)-1) true; else false
		logging.debug("checking spoofedBetweenAttackergw. Is %s between or is a gateway (or equal to either) %s to %s:",victim,src,attackNode)
		subPath = []
		if victim == src:
			flowDescriptionAttributes["spoofedBetweenAttackergw"]="True"
		else:
			#real path
			pathA = getPathThroughGW(src,attackNode)
			#path to "between" node
			pathB = getPathThroughGW(src,victim)
			#now check if pathA starts with pathB-1
			if len(pathB) == 0 and len(pathB) > len(pathA):
				flowDescriptionAttributes["spoofedBetweenAttackergw"]="False"
			else:
				pathB = pathB[:len(pathB)-1]
				#check if param1 is a subpath of param2
				subPath = getSubPath(pathB, pathA)
				logging.debug("subPath of: %s %s %s \nSUBPATH: %s",src,victim,attackNode,subPath)
				flowDescriptionAttributes["spoofedBetweenAttackergw"]="False"
		if len(subPath) == 0:
			flowDescriptionAttributes["spoofedBetweenAttackergw"]="False"
		else:
			flowDescriptionAttributes["spoofedBetweenAttackergw"]="True"
		logging.debug("spoofedBetweenAttackergw %s",flowDescriptionAttributes["spoofedBetweenAttackergw"])

#######
		logging.debug("checking isDstBetweenSpoofedAndAttackergw Is: %s between or is a gateway (or equal to either) %s to %s",victim,dst,attackNode)
		subPath = []
		if victim == dst:
			flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]="True"
		else:
			#real path
			pathA = getPathThroughGW(dst,attackNode)
			#path to "between" node
			pathB = getPathThroughGW(dst,victim)
			#now check if pathA starts with pathB-1
			if len(pathB) == 0 and len(pathB) > len(pathA):
				flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]="False"
			else:
				pathB = pathB[:len(pathB)-1]
				#check if param1 is a subpath of param2
				subPath = getSubPath(pathB, pathA)
				logging.debug("subPath of: %s %s %s \nSUBPATH: %s",dst,victim,attackNode,subPath)
				flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]="False"
		if len(subPath) == 0:
			flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]="False"
		else:
			flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]="True"
		logging.debug("isDstBetweenSpoofedAndAttackergw %s",flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"])

#######
		logging.debug("checking isAttackerBetweenSpoofedAndDst. Is: %s between (or equal to either) %s to %s",attackNode,victim,dst)
		if attackNode == victim:
			flowDescriptionAttributes["isAttackerBetweenSpoofedAndDst"]="True"
		elif attackNode in getPathThroughGW(victim,dst):
			flowDescriptionAttributes["isAttackerBetweenSpoofedAndDst"]="True"
		else:
			flowDescriptionAttributes["isAttackerBetweenSpoofedAndDst"]="False"
		logging.debug("isAttackerBetweenSpoofedAndDst %s",flowDescriptionAttributes["isAttackerBetweenSpoofedAndDst"])

#######

		logging.debug("checking isAttackerBetweenSpoofedAndDstgw Is: %s between or is a gateway (or equal to either) %s to %s",attackNode,victim,dst)
		subPath = []
		if attackNode == victim:
			flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]="True"
		else:
			#real path
			pathA = getPathThroughGW(victim,dst)
			#path to "between" node
			pathB = getPathThroughGW(victim,attackNode)
			#now check if pathA starts with pathB-1
			if len(pathB) == 0 and len(pathB) > len(pathA):
				flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]="False"
			else:
				pathB = pathB[:len(pathB)-1]
				#check if param1 is a subpath of param2
				subPath = getSubPath(pathB, pathA)
				logging.debug("subPath of: %s %s %s \nSUBPATH: %s",victim,attackNode,dst,subPath)
				flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]="False"
		if len(subPath) == 0:
			flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]="False"
		else:
			flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]="True"
		logging.debug("isAttackerBetweenSpoofedAndDstgw %s",flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"])
	
		
#######
#21. isSrcBetweenSpoofedAndDst	-- src between vic and dst
#######
		logging.debug("checking isSrcBetweenSpoofedAndDst. Is: %s between (or equal to either) %s to %s",src,victim,dst)
		if src == victim:
			flowDescriptionAttributes["isSrcBetweenSpoofedAndDst"]="True"
		elif src in getPathThroughGW(victim,dst):
			flowDescriptionAttributes["isSrcBetweenSpoofedAndDst"]="True"
		else:
			flowDescriptionAttributes["isSrcBetweenSpoofedAndDst"]="False"
		logging.debug("isSrcBetweenSpoofedAndDst %s",flowDescriptionAttributes["isSrcBetweenSpoofedAndDst"])


#######	
#22. flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]	-- src a gw of any node between vic and dst

		logging.debug("checking isSrcBetweenSpoofedAndDstgw Is: %s between or is a gateway (or equal to either) %s to %s",src,victim,dst)
		subPath = []
		if src == victim:
			flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]="True"
		else:
			#real path
			pathA = getPathThroughGW(victim,dst)
			#path to "between" node
			pathB = getPathThroughGW(victim,src)
			#now check if pathA starts with pathB-1
			if len(pathB) == 0 and len(pathB) > len(pathA):
				flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]="False"
			else:
				pathB = pathB[:len(pathB)-1]
				#check if param1 is a subpath of param2
				subPath = getSubPath(pathB, pathA)
				logging.debug("subPath of: %s %s %s \nSUBPATH: %s",victim,src,dst,subPath)
				flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]="False"
		if len(subPath) == 0:
			flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]="False"
		else:
			flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]="True"
		logging.debug("isSrcBetweenSpoofedAndDstgw %s",flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]	)

#######	
#23. flowDescriptionAttributes["altPathWithoutAttacker"]

#clone the graph, remove the attacker and then check if a path exists from src to dst
		logging.debug("checking altPathWithoutAttacker: attackNode %s src: %s dst: %s",attackNode,src,dst)
		if not nx.has_path(G,src,dst):
			flowDescriptionAttributes["altPathWithoutAttacker"]="False"
		else:
			tmpGraph = G.copy()
			tmpGraph.remove_node(attackNode)
			if not nx.has_path(tmpGraph,src,dst):
				flowDescriptionAttributes["altPathWithoutAttacker"]="False"
			else:
				flowDescriptionAttributes["altPathWithoutAttacker"]="True"
		logging.debug("altPathWithoutAttacker %s",flowDescriptionAttributes["altPathWithoutAttacker"])
		logging.debug("\n\n")
		
		#######now generate XML tags:
		#print "Here!!!"
		flowDescriptionAttributesXML = etree.SubElement(attributesXML, "FlowDescriptionAttributes")
		for attribute in flowDescriptionAttributes:
			attributeXML = etree.SubElement(flowDescriptionAttributesXML, "Attribute")
			nameXML = etree.SubElement(attributeXML, "Name")
			nameXML.text = attribute
			valueXML = etree.SubElement(attributeXML, "Value")
			valueXML.text = flowDescriptionAttributes[attribute]


#first read the input configuration xml file
def readConfig(filename):
	global nodes
	global attackName
	global victim
	global attackNode
	global flows
	
	tree = ET.parse(filename)
	root = tree.getroot()
	scenarioConfig = root.find('scenario-config')
	attackName = scenarioConfig.find('attack-name').text.rstrip().lstrip()
	if len(attackName.split("spoofingAttack.sh")) > 1:
		#####Temporary hack, won't work if IPs are different!!!!!#######
		victim = IPNetwork("10.0.0."+""+attackName.split("spoofingAttack.sh")[1])
	attackNode = IPNetwork(scenarioConfig.find('attack-node').text.rstrip().lstrip())
	trafficProfile = scenarioConfig.find('traffic-profile')
	#extract the traffic flows
	for flow in trafficProfile.findall('flow'):
		flows.append((IPNetwork(flow.find('src').text.rstrip().lstrip()),IPNetwork(flow.find('dst').text.rstrip().lstrip()),flow.find('type').text.rstrip().lstrip()))

	#extract node information
	for node in scenarioConfig.findall('node'):
		name = node.find('name')
		nodeRoutes = node.find('routes').text.rstrip().lstrip()
		nodeIP = IPNetwork(node.find('ip-addresses').text.rstrip().lstrip())
		#want to keep track of IP addresses and their subnets for path lookup
		nodes[nodeIP.ip] = nodeIP.cidr
		#Extract links and metrics and store results in gateways{}
		extractLinksfromRoutes(nodeIP, nodeRoutes)
		nodes[name.text.rstrip().lstrip()] = 'test'


#Will eventually convert print to logging
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
filename = sys.argv[1]
readConfig(filename)
logging.debug("Nodes\n%s", nodes)
logging.debug("\nGateways\n%s",gateways)
logging.debug("\nDirect Links\n%s",directLinks)
logging.debug("\nG\n%s",G.edges())

generateParametersFromTrafficProfile()

print etree.tostring(attributesXML,pretty_print='true')
