#!/usr/bin/python
import time
import thread
import sys
import commands

myIPs = sys.argv[1:]
startTimeSec=-1
prevTimeSec=-1

lines = []
currTimeSec = 0
totalDelay = 0
totalMissedPackets = 0
totalNumPackets =0
totalOOO =0
flows = {}
seqs = {}
routes = {}

attackRunning = "none"

def processLines():
    global currTimeSec
    global lines
    global flows
    global attackRunning
    global totalDelay
    global totalMissedPackets
    global seqs
    global totalOOO
    global totalNumPackets
    global routes
    
    getRoutes()
    getTraffTypeCounts()
    getAttackRunning()
    print str((int(str(currTimeSec).split(".")[0])-int(str(startTimeSec).split(".")[0])))+";"+str(flows) + ";" +str(totalDelay)+";"+str(totalMissedPackets)+ ";" +str(totalOOO)+ ";" +str(totalNumPackets)+ ";" +str(attackRunning)+ ";" +str(routes)
    #print "Lines",lines

    lines = []
    flows = {}
    routes = {}
    attackRunning = "none"
    totalDelay = 0
    totalMissedPackets = 0
    totalNumPackets=0
    totalOOO =0
    
def getTraffTypeCounts():
    global lines
    global currTimeSec
    global totalDelay
    global totalMissedPackets
    global flows
    global seqs
    global totalNumPackets
    global totalOOO
    
    for line in lines:
        #split the line by space
        splitLine = line.split(" ")
        proto = splitLine[2].split(">")[1]
        #flow = splitLine[3].split(">")[1]
        seq = int(splitLine[4].split(">")[1])
        src = splitLine[5].split(">")[1].split("/")[0]
        dst = splitLine[6].split(">")[1].split("/")[0] #should be current node
        flow = src+"_"+dst
        dist = "*"
        if src in routes:
            dist = routes[src][0]
        sentTime = splitLine[7].split(">")[1]
        
        sentTimeSplitSec = sentTime.split(":")
        sentTimeSec = 360*int(sentTimeSplitSec[0]) + 60*int(sentTimeSplitSec[1]) + float(sentTimeSplitSec[2]) 
        
#        print "proto",proto
        #print "flow",flow,"seq",seq
        #print "seq",seq
#        print "sentTime",sentTime
#        print "currTimeSec",currTimeSec
        
        delay = currTimeSec-sentTimeSec
        
        totalDelay += delay
        
        missedPackets = 0
        numPackets=1
        totalNumPackets+=1;
        ooo = 0
        #TODO: make sure flow is in seqs, if not, set to first, if it is, take first val
        
        if flow not in seqs:
            seqs[flow] = seq

#        if seq > seqs[flow]+1:
#            print "Flow",flow,"Missed Packets:", seq,seqs[flow]
        if seq > seqs[flow]:
            missedPackets = seq - seqs[flow] - 1
            totalMissedPackets+=missedPackets
            #print "MissedPackets:",missedPackets
            seqs[flow] = seq  
        else:
            ooo+=1
            totalOOO+=1
        if (flow,proto) in flows:    
            delay += flows[(flow,proto)][0]
            missedPackets += flows[(flow,proto)][1]
            ooo+=flows[(flow,proto)][2]
            numPackets+=flows[(flow,proto)][3]
            flows[(flow,proto)] = (delay,missedPackets,ooo,numPackets,dist)
        else:
              flows[(flow,proto)] = (delay,missedPackets,ooo,numPackets,dist)

    #print "Seqs",seqs
    
def getAttackRunning():
    global attackRunning
    attackRunning = commands.getoutput("cat /tmp/attack.txt")
    if "No such file or directory" in attackRunning:
        attackRunning = "none"

def getRoutes():
    global routes
    maxHopTraff = {}
    hopNeighbors = {}
    routes = commands.getoutput("route -n | awk 'NR>2 {print $1\",\"$2\",\"$5}'").split("\n")
    #looks like: ROUTES ['10.0.2.0,*,1', 'link-local,*,1000', 'default,10.0.2.2,0']
    ipHopDict = {}
    for routeLine in routes:
        splitLine = routeLine.split(",")
        #if hop exists
        if splitLine[2] in hopNeighbors:
            #if ip does not exist in hop
            if splitLine[0] not in hopNeighbors[splitLine[2]]:
                 hopNeighbors[splitLine[2]][splitLine[0]] = (0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        else:
            hopNeighbors[splitLine[2]] = {splitLine[0]: (0,0,0,0,0,0,0,0,0,0,0,0,0,0)}
            maxHopTraff[splitLine[2]] = ("",-1)
        if splitLine[0] not in ipHopDict:
            ipHopDict[splitLine[0]] = (splitLine[2],splitLine[1])
    routes = ipHopDict



while 1:
    line = sys.stdin.readline()
    
    if len(line.split(" ")) == 11:
        #get time and convert to seconds
        currTime = line.split(" ")[0]
        currTimeSplitSec = currTime.split(":")
        currTimeSec = 360*int(currTimeSplitSec[0]) + 60*int(currTimeSplitSec[1]) + float(currTimeSplitSec[2]) 
        if prevTimeSec == -1:
            prevTimeSec = currTimeSec
            startTimeSec = currTimeSec
        else:
            if int(str(currTimeSec).split(".")[0]) >= int(str(prevTimeSec).split(".")[0]) + 1:
                prevTimeSec = currTimeSec
                processLines()
        lines.append(line)
