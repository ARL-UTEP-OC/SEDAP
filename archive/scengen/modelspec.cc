#!/usr/bin/python
import ast
import sys

nBeforeAttack = sys.argv[1]
mAfterAttack = sys.argv[2]
attackNodeNum = sys.argv[3]
maxHopNum = 5

myNetworkStateRaw = [] #queue of tuples that will keep x entries before attack
attackStartTime = -1

##Read network state up to the attack from the attacker's view
attackerFile = open('n'+attackNodeNum+'.capture')
for line in attackerFile.readlines():
    hops = ast.literal_eval(line.split(";")[1])
    hopToHop = ast.literal_eval(line.split(";")[2])
    trafficFromMe = ast.literal_eval(line.split(";")[3])
    trafficToMe = ast.literal_eval(line.split(";")[4])
    attackRunning = line.split(";")[5]
    #keep only nBeforeAttack entries in the queue
    if len(myNetworkStateRaw) >= int(nBeforeAttack):
        myNetworkStateRaw.pop()
    myNetworkStateRaw.append((hops,hopToHop,trafficFromMe,trafficToMe))
    if not attackRunning.startswith("no"):
        #we know the attack started here, lets process the queue and also 
        #see what effect the attack had on other nodes (read in their mgen logs)
        attackStartTime = ast.literal_eval(line.split(";")[0])
        attackerFile.close()
        break
#Read effect of attack on other nodes:




print "Attack started at: ",attackStartTime
def getNumNodesPerHop():
    #get num nodes in each hop
    global myNetworkStateRaw
    global numNodes
    #global hops
    totalNumNodes = {}
    for instance in myNetworkStateRaw:
        hops = instance[0]
        for hop in hops:
            numNodes[hop] = len(hops[hop])
            if hop in totalNumNodes:
                totalNumNodes[hop] += numNodes[hop]
            else: totalNumNodes[hop] = numNodes[hop]
    for i in totalNumNodes:
        totalNumNodes[i] = float(totalNumNodes[i])/float(nBeforeAttack)
    numNodes = totalNumNodes

def getTCPUDPCounts():
    #first from me
    #to me
    global myNetworkStateRaw
    global tcpFromCounts
    global udpFromCounts
    global tcpToCounts
    global udpToCounts
    
    totalTcpFromCounts = {}
    totalUdpFromCounts = {}
    totalTcpToCounts = {}
    totalUdpToCounts = {}
    #print "len(myRaw)",len(myNetworkStateRaw)
    
    for instance in myNetworkStateRaw:
        hops = instance[0]
        for hop in hops:
            tcpFromCounts[hop] = 0
            udpFromCounts[hop] = 0
            tcpToCounts[hop] = 0
            udpToCounts[hop] = 0
            #print "sum: ", 
            for myVar in hops[hop].values():
            
                tcpFromCounts[hop]+=myVar[1]
                udpFromCounts[hop]+=myVar[4]
                tcpToCounts[hop]+=myVar[8]
                udpToCounts[hop]+=myVar[11]
                if hop in totalTcpFromCounts:
                    totalTcpFromCounts[hop] += myVar[1]
                else: totalTcpFromCounts[hop] = myVar[1]
                
                if hop in totalUdpFromCounts:
                    totalUdpFromCounts[hop] += myVar[4]
                else: totalUdpFromCounts[hop] = myVar[4]
                #print "totalUDPFrom",hop," now: ", totalUdpFromCounts[hop]
                
                if hop in totalTcpToCounts:
                    totalTcpToCounts[hop] += myVar[8]
                else: totalTcpToCounts[hop] = myVar[8]                
                
                if hop in totalUdpToCounts:
                    totalUdpToCounts[hop] += myVar[11]
                else: totalUdpToCounts[hop] = myVar[11]                
    for i in totalTcpFromCounts:
        totalTcpFromCounts[i] = float(totalTcpFromCounts[i])/float(nBeforeAttack)          
    for i in totalUdpFromCounts:
        tot