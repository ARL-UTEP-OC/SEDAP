#!/usr/bin/python
# Author(s): J. Acosta, B. Medina
# Date: 25 Jan 2012
# Input: Number of nodes
# Output: N files, where N = number of nodes specified by user
# Description: This scripts uses specified communication patterns and ports to create a file per node specifiying the following:
#              (1) Nodes and ports it sends messages to (2) Nodes and ports that listen to this node
# Assumption(s): (1) number of outlfows = number of inflows (2) starting port = 6000

import sys
import os

### import configuration from file - Edgar P.
import json

data_str =  open('../configuration/configuration.json','r')    
# loading json data
json_data = json.load(data_str)

protocol = json_data["flows"]["protocol"]
wireType = json_data["flows"]["wire-type"]
portStart = int(json_data["flows"]["initial-port"])

outFlowPattern = []
portPattern = []
protocolPattern = []

traffic_nodes =  json_data["flows"]["traffic-nodes"]
numNodes = len(traffic_nodes)

for nodeNum in range(1, numNodes):
	outFlowPattern.append(nodeNum)
        portPattern.append(nodeNum)
	protocolPattern.append(protocol)
print outFlowPattern
print portPattern
print protocolPattern

### end of reading configuration

# outFlowPattern specifies which nodes to send to relative to the current node: Example [-1, +1, +2] means send to previous, next and next next
# Note: node 1's previous node is node N, where N = number of nodes
#outFlowPattern = [-1, 1, 2, 3,4,5,6,7,8]
#outFlowPattern = [-1, 1, 2]


# portPattern specifies which port to use next relative to the starting port
# Note: portPattern list must be of the same size as the outFlowPattern
# Example: outFlowPattern = [-1, +1, +2] & portPattern = [0, +1, +2] ==> use port portStart to send to previous node (-1), use port (portstart + 1) to send to next node (+1), and use port (portStart + 2) to send to next next node (+2)
#portPattern = [0, 1, 2, 3,4,5,6,7,8]
#portPattern = [0, 1, 2]

#add a protocolPattern, where 0 is udp and 1 is tcp
#protocolPattern = ["UDP","UDP","UDP","UDP","UDP","UDP","UDP","UDP","UDP","UDP","UDP","UDP"]

# outFlowHash and inFlowHash are hash tables to store all send and listen communications specifying nodes and ports involved
outFlowHash = {}
inFlowHash = {}

for node in range(1, numNodes + 1):

    #initialize list elements to empty lists
    if node not in outFlowHash:
        outFlowHash[node] = []
    for nodeIndex in outFlowPattern:
        receivingNode = (node + nodeIndex) % numNodes
#	print 'node : ', node, '  nodeIndex: ', nodeIndex, ' numNodes: ' , numNodes
#	print 'receivingNode: ', receivingNode
        if receivingNode == 0:
            receivingNode = numNodes
        if receivingNode not in inFlowHash: 
            inFlowHash[receivingNode] = [] #if node k sends to node j then node j must listen to node k

    # process and store comunications data: outflow
    for index in range(len(outFlowPattern)):
#	print 'node : ', node,' outFlowPattern[index]: ', outFlowPattern[index]
        receivingNode = (node + outFlowPattern[index]) % numNodes
#	print 'receivingNode: ', receivingNode
        if receivingNode == 0:
            receivingNode = numNodes
        outFlowHash[node].append((receivingNode, portStart + portPattern[index],protocolPattern[index]))
        inFlowHash[receivingNode].append((node, portStart + portPattern[index],protocolPattern[index]))
    portStart += len(portPattern) #will fail if port pattern is not equal to [0, 1, 2, ..., N], need another mechanism to update if different pattern


#write files
try:
    os.mkdir("flows")
except:
    #directory already exists
    pass
index = 1
for hashkey in outFlowHash:
	f = open("flows/flown" + str(hashkey) + ".mgn", 'w')
	f.write("#flow " + str(hashkey) + "\n")
	sendingTo = outFlowHash[hashkey]
	listeningTo = inFlowHash[hashkey]
    
	# assumes a pair (node number, port number)
	for pairIndex in range(len(listeningTo)):
	#This is the problem, on the incoming connections, unless the population method is changed, the TCP is not always the first!
		f.write("0.0 LISTEN " + str(listeningTo[pairIndex][2]) + " " + str(listeningTo[pairIndex][1]) + " # Node " + str(listeningTo[pairIndex][0]) + "\n")
	f.write("\n")
    
	for pairIndex in range(len(sendingTo)):
		destination = " DST " + traffic_nodes[int(sendingTo[pairIndex][0])-1]
		f.write("30.0 ON " + str(index) + " " + str(sendingTo[pairIndex][2]) + destination + "/" + str(sendingTo[pairIndex][1]) + " PERIODIC [50.0 1280]\n")
		index += 1
    
	f.close()

#print hashes
print "OUTFLOW HASH"
print outFlowHash
print "\n"
print "INFLOW HASH"
print inFlowHash
