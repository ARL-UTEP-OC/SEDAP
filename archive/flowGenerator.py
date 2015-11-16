#!/usr/bin/python
import time
import thread
import sys
import commands
import ast


numNodes = sys.argv[1]
numFlowsOutPerNode = sys.argv[2]

numNodes = int(numNodes) + 1
numFlowsOutPerNode = int(numFlowsOutPerNode)
 
portStart = 6000
currPort = portStart
outFlows = {} #will contain node, (listens), (sends)
inFlows = {}


def inc(currVal,whichToSkip):
    print "currBefore",currVal,whichToSkip
    currVal +=1
    if currVal >= numNodes:
        currVal =1
    if currVal == whichToSkip:
        curVal +=1
    if currVal >= numNodes:
        currVal =1
    print "currAfter",currVal
    return currVal

for i in range(1, int(numNodes)):
     localOutLeft = numFlowsOutPerNode
     currRecvNode = i
          
     while localOutLeft !=0:
         #add outs to curr node
         currRecvNode = inc(currRecvNode,i)
         if i not in outFlows:
             outFlows[i] = [(currRecvNode,currPort)]
         else: outFlows[i].append((currRecvNode,currPort))
         
         if currRecvNode not in inFlows:
             inFlows[currRecvNode] = [(i,currPort)]
         else: inFlows[currRecvNode].append((i,currPort))
         localOutLeft -= 1
         currPort +=1
         print i,localOutLeft
         
print outFlows
print inFlows