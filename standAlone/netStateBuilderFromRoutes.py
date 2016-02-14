#!/usr/bin/python
import sys
import networkx as nx
import xml.etree.ElementTree as ET
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

#parameters for output
fromHop=''
toHop=''
typeName=''
distance=''
passthrough=''
srcSpoofed=''
destSpoofed=''
hopsToSpoofed=''
hopsFromSpoofedToDest=''
spoofedBetweenAttacker=''
isDstBetweenSpoofedAndAttacker=''
spoofedBetweenAttackergw=''
isDstBetweenSpoofedAndAttackergw=''
isAttackerBetweenSpoofedAndDst=''
isAttackerBetweenSpoofedAndDstgw=''
isSrcBetweenSpoofedAndDst=''
isSrcBetweenSpoofedAndDstgw=''
altPathWithoutAttacker=''


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
	global fromHop
	global toHop
	global typeName
	global distance
	global passthrough
	global srcSpoofed
	global destSpoofed
	global hopsToSpoofed
	global hopsFromSpoofedToDest
	global spoofedBetweenAttacker
	global isDstBetweenSpoofedAndAttacker
	global spoofedBetweenAttackergw
	global isDstBetweenSpoofedAndAttackergw
	global isAttackerBetweenSpoofedAndDst
	global isAttackerBetweenSpoofedAndDstgw
	global isSrcBetweenSpoofedAndDst
	global isSrcBetweenSpoofedAndDstgw
	global altPathWithoutAttacker
	
	for flow in flows:
		#fromHop
		src = flow[0]
		dst = flow[1]
		
		print "looking for: ",(attackNode,src)
		if ((attackNode,src)) in directLinks:
			fromHop = directLinks[(attackNode,src)]
		elif ((attackNode,src)) in gateways:
			fromHop = gateways[(attackNode,src)]
		else:
			print fromHop,"not found"
			exit
		print "fromHop",fromHop

		#toHop
		print "looking for: ",(attackNode,dst)
		if ((attackNode,dst)) in directLinks:
			toHop = directLinks[(attackNode,dst)]
		elif ((attackNode,dst)) in gateways:
			toHop = gateways[(attackNode,dst)]
		else:
			print toHop,"not found"
			exit
		print "toHop",toHop
		
		#type
		typeName = flow[2]
		print "type",typeName
		
		#distance
		print "looking for: ",(src,dst)
		if ((src,dst)) in directLinks:
			distance = directLinks[(flow[0],dst)][1]
		elif ((src,dst)) in gateways:
			distance = gateways[(src,dst)][1]
		else:
			print distance,"not found"
			exit
		print "distance",distance
		###path function test
		print "looking for path: ",(src,dst)
		print "\nPath\n",getPathThroughGW(src, dst)
		###
		
		print "\npassthrough check: ",attackNode, "in", (src,dst)
		if attackNode in getPathThroughGW(src,dst):
			passthrough=True
		else:
			passthrough=False
########The following parameters are only valid if attack is spoofing#####
		print "\nsrc spoofed: ",src, victim
		if src == victim:
			srcSpoofed=True
		else:
			srcSpoofed=False
		print "srcSpoofed",srcSpoofed

		print "\ndst spoofed: ",dst, victim
		if dst == victim:
			dstSpoofed=True
		else:
			dstSpoofed=False
		print "dstSpoofed",dstSpoofed

		print "checking hopsToSpoofed from:",attackNode,"to",victim
		if (attackNode,victim) in directLinks:
			hopsToSpoofed=directLinks[(attackNode,victim)][1]
		elif (attackNode,victim) in gateways:
			hopsToSpoofed=gateways[(attackNode,victim)][1]
		else: 
			hopsToSpoofed='-1'
		print "hopsToSpoofed",hopsToSpoofed
			
		print "checking hopsFromSpoofedToDest from:",victim,"to",dst
		if (victim,dst) in directLinks:
			hopsFromSpoofedToDest=directLinks[(victim,dst)][1]
		elif (victim,dst) in gateways:
			hopsFromSpoofedToDest=gateways[(victim,dst)][1]
		else: 
			hopsFromSpoofedToDest='-1'
		print "hopsFromSpoofedToDest",hopsFromSpoofedToDest		
		
		print "checking spoofedBetweenAttacker. Is:",victim,"between (or equal to either)",src,"to",attackNode
		if victim == src:
			spoofedBetweenAttacker=True
		elif victim in getPathThroughGW(src,attackNode):
			spoofedBetweenAttacker=True
		else:
			spoofedBetweenAttacker=False
		print "spoofedBetweenAttacker",spoofedBetweenAttacker
		
		print "checking isDstBetweenSpoofedAndAttacker. Is:",dst,"between (or equal to either)",victim,"to",attackNode
		if dst == victim:
			isDstBetweenSpoofedAndAttacker=True
		elif dst in getPathThroughGW(victim,attackNode):
			isDstBetweenSpoofedAndAttacker=True
		else:
			isDstBetweenSpoofedAndAttacker=False
		print "isDstBetweenSpoofedAndAttacker",isDstBetweenSpoofedAndAttacker
		
#######
		#algorithm used to check: if path(src,dst) startswith(path(src,att)-1) true; else false
		print "checking spoofedBetweenAttackergw. Is:",victim,"between or is a gateway (or equal to either)",src,"to",attackNode
		subPath = []
		if victim == src:
			spoofedBetweenAttackergw=True
		else:
			#real path
			pathA = getPathThroughGW(src,attackNode)
			#path to "between" node
			pathB = getPathThroughGW(src,victim)
			#now check if pathA starts with pathB-1
			if len(pathB) == 0 and len(pathB) > len(pathA):
				spoofedBetweenAttackergw=False
			else:
				pathB = pathB[:len(pathB)-1]
				#check if param1 is a subpath of param2
				subPath = getSubPath(pathB, pathA)
				print "subPath of:",src,victim,attackNode,"\nSUBPATH:",subPath
				spoofedBetweenAttackergw=False
		if len(subPath) == 0:
			spoofedBetweenAttackergw=False
		else:
			spoofedBetweenAttackergw=True
		print "spoofedBetweenAttackergw",spoofedBetweenAttackergw

#######
		print "checking isDstBetweenSpoofedAndAttackergw Is:",victim,"between or is a gateway (or equal to either)",dst,"to",attackNode
		subPath = []
		if victim == dst:
			isDstBetweenSpoofedAndAttackergw=True
		else:
			#real path
			pathA = getPathThroughGW(dst,attackNode)
			#path to "between" node
			pathB = getPathThroughGW(dst,victim)
			#now check if pathA starts with pathB-1
			if len(pathB) == 0 and len(pathB) > len(pathA):
				isDstBetweenSpoofedAndAttackergw=False
			else:
				pathB = pathB[:len(pathB)-1]
				#check if param1 is a subpath of param2
				subPath = getSubPath(pathB, pathA)
				print "subPath of:",dst,victim,attackNode,"\nSUBPATH:",subPath
				isDstBetweenSpoofedAndAttackergw=False
		if len(subPath) == 0:
			isDstBetweenSpoofedAndAttackergw=False
		else:
			isDstBetweenSpoofedAndAttackergw=True
		print "isDstBetweenSpoofedAndAttackergw",isDstBetweenSpoofedAndAttackergw

#######
		print "checking isAttackerBetweenSpoofedAndDst. Is:",attackNode,"between (or equal to either)",victim,"to",dst
		if attackNode == victim:
			isAttackerBetweenSpoofedAndDst=True
		elif attackNode in getPathThroughGW(victim,dst):
			isAttackerBetweenSpoofedAndDst=True
		else:
			isAttackerBetweenSpoofedAndDst=False
		print "isAttackerBetweenSpoofedAndDst",isAttackerBetweenSpoofedAndDst

#######

		print "checking isAttackerBetweenSpoofedAndDstgw Is:",attackNode,"between or is a gateway (or equal to either)",victim,"to",dst
		subPath = []
		if attackNode == victim:
			isAttackerBetweenSpoofedAndDstgw=True
		else:
			#real path
			pathA = getPathThroughGW(victim,dst)
			#path to "between" node
			pathB = getPathThroughGW(victim,attackNode)
			#now check if pathA starts with pathB-1
			if len(pathB) == 0 and len(pathB) > len(pathA):
				isAttackerBetweenSpoofedAndDstgw=False
			else:
				pathB = pathB[:len(pathB)-1]
				#check if param1 is a subpath of param2
				subPath = getSubPath(pathB, pathA)
				print "subPath of:",victim,attackNode,dst,"\nSUBPATH:",subPath
				isAttackerBetweenSpoofedAndDstgw=False
		if len(subPath) == 0:
			isAttackerBetweenSpoofedAndDstgw=False
		else:
			isAttackerBetweenSpoofedAndDstgw=True
		print "isAttackerBetweenSpoofedAndDstgw",isAttackerBetweenSpoofedAndDstgw
	
		
#######
#21. isSrcBetweenSpoofedAndDst	-- src between vic and dst
#######
		print "checking isSrcBetweenSpoofedAndDst. Is:",src,"between (or equal to either)",victim,"to",dst
		if src == victim:
			isSrcBetweenSpoofedAndDst=True
		elif src in getPathThroughGW(victim,dst):
			isSrcBetweenSpoofedAndDst=True
		else:
			isSrcBetweenSpoofedAndDst=False
		print "isSrcBetweenSpoofedAndDst",isSrcBetweenSpoofedAndDst


#######	
#22. isSrcBetweenSpoofedAndDstgw	-- src a gw of any node between vic and dst

		print "checking isSrcBetweenSpoofedAndDstgw Is:",src,"between or is a gateway (or equal to either)",victim,"to",dst
		subPath = []
		if src == victim:
			isSrcBetweenSpoofedAndDstgw=True
		else:
			#real path
			pathA = getPathThroughGW(victim,dst)
			#path to "between" node
			pathB = getPathThroughGW(victim,src)
			#now check if pathA starts with pathB-1
			if len(pathB) == 0 and len(pathB) > len(pathA):
				isSrcBetweenSpoofedAndDstgw=False
			else:
				pathB = pathB[:len(pathB)-1]
				#check if param1 is a subpath of param2
				subPath = getSubPath(pathB, pathA)
				print "subPath of:",victim,src,dst,"\nSUBPATH:",subPath
				isSrcBetweenSpoofedAndDstgw=False
		if len(subPath) == 0:
			isSrcBetweenSpoofedAndDstgw=False
		else:
			isSrcBetweenSpoofedAndDstgw=True
		print "isSrcBetweenSpoofedAndDstgw",isSrcBetweenSpoofedAndDstgw	

#######	
#23. altPathWithoutAttacker

#clone the graph, remove the attacker and then check if a path exists from src to dst
		print "checking altPathWithoutAttacker: attackNode",attackNode,"src:",src,"dst:",dst
		if not nx.has_path(G,src,dst):
			altPathWithoutAttacker=False
		else:
			tmpGraph = G.copy()
			tmpGraph.remove_node(attackNode)
			if not nx.has_path(tmpGraph,src,dst):
				altPathWithoutAttacker=False
			else:
				altPathWithoutAttacker=True
		print "altPathWithoutAttacker",altPathWithoutAttacker		
		print "\n\n"

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
print "Nodes\n", nodes
print "\nGateways\n",gateways
print "\nDirect Links\n",directLinks
print "\nG\n",G.edges()

generateParametersFromTrafficProfile()
