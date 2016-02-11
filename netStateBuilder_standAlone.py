#!/usr/bin/python
import time
import thread
import sys
import commands
import ast
import networkx as nx
import xml.etree.ElementTree as ET

instance = ""

#globals
gateways = {} #(src, dest) -> (gateway, metric)
directLinks = {} #(src, dest) -> ('0.0.0.0', metric)
G = nx.Graph()
nodes = {} 

attackName = ""
attackNode = ""
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
isAttackerBetweenSpoofedAndAttacker=''
isAttackerBetweenSpoofedAndAttackergw=''
isSrcBetweenSpoofedAndDst=''
isSrcBetweenSpoofedAndDstgw=''
altPathWithoutAttacker=''


def extractLinksfromRoutes(nodeIPs, routes):
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
		if elements[1] == '0.0.0.0':
			directLinks[(nodeIPs,elements[0])] = (elements[1], elements[4])
			#also add direct links to our networkx graph for later processing
			G.add_edge(nodeIPs,elements[0])
		#otherwise, this we extract the gateway
		else:
			gateways[(nodeIPs,elements[0])] = (elements[1], elements[4])

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
	global isAttackerBetweenSpoofedAndAttacker
	global isAttackerBetweenSpoofedAndAttackergw
	global isSrcBetweenSpoofedAndDst
	global isSrcBetweenSpoofedAndDstgw
	global altPathWithoutAttacker
	
	for flow in flows:
		#fromHop
		print "looking for: ",(attackNode,flow[0].split('/')[0])
		if ((attackNode,flow[0].split('/')[0])) in directLinks:
			fromHop = directLinks[(attackNode,flow[0].split('/')[0])]
		elif ((attackNode,flow[0].split('/')[0])) in gateways:
			fromHop = gateways[(attackNode,flow[0].split('/')[0])]
		else:
			print fromHop,"not found"
			exit
		print "fromHop",fromHop

		#toHop
		print "looking for: ",(attackNode,flow[1].split('/')[0])
		if ((attackNode,flow[1].split('/')[0])) in directLinks:
			toHop = directLinks[(attackNode,flow[1].split('/')[0])]
		elif ((attackNode,flow[1].split('/')[0])) in gateways:
			toHop = gateways[(attackNode,flow[1].split('/')[0])]
		else:
			print toHop,"not found"
			exit
		print "toHop",toHop
		
		#type
		typeName = flow[2]
		print "type",typeName
		
		#distance
		print "looking for: ",(flow[0],flow[1].split('/')[0])
		if ((flow[0],flow[1].split('/')[0])) in directLinks:
			distance = directLinks[(flow[0],flow[1].split('/')[0])][1]
		elif ((flow[0],flow[1].split('/')[0])) in gateways:
			distance = gateways[(flow[0],flow[1].split('/')[0])][1]
		else:
			print distance,"not found"
			exit
		print "distance",distance
		
		
		
		print "\n\n"

#first read the input configuration xml file
def readConfig(filename):
	global nodes
	global attackName
	global attackNode
	global flows
	
	tree = ET.parse(filename)
	root = tree.getroot()
	scenarioConfig = root.find('scenario-config')
	attackName = scenarioConfig.find('attack-name').text.rstrip().lstrip()
	attackNode = scenarioConfig.find('attack-node').text.rstrip().lstrip()
	trafficProfile = scenarioConfig.find('traffic-profile')
	#extract the traffic flows
	for flow in trafficProfile.findall('flow'):
		flows.append((flow.find('src').text.rstrip().lstrip(),flow.find('dst').text.rstrip().lstrip(),flow.find('type').text.rstrip().lstrip()))

	#extract node information
	for node in scenarioConfig.findall('node'):
		name = node.find('name')
		nodeRoutes = node.find('routes').text.rstrip().lstrip()
		nodeIPs = node.find('ip-addresses').text.rstrip().lstrip()
		#Extract links and metrics and store results in gateways{}
		extractLinksfromRoutes(nodeIPs, nodeRoutes)
		nodes[name.text.rstrip().lstrip()] = 'test'

filename = 'netStateBuilderStandAlone.xml'
readConfig(filename)
print "Gateways\n",gateways
print "\nDirect Links\n",directLinks
print "\nG\n",G.edges()

generateParametersFromTrafficProfile()
