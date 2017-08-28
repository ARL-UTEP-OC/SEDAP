#!/usr/bin/python
import time
import thread
import sys
import commands

filePath = sys.argv[1]
myIPs = sys.argv[2:]
startTime=int(commands.getoutput("date +%s"))
prevTime=startTime

lines = []
currTime = 0

trafficFromMe = (0,0,0,0,0,0)
trafficToMe = (0,0,0,0,0,0)
attackRunning = "none"

flows = {}
routes = {}
hopNeighbors = {}
hopTraff = {}
#will hold hop/(ip,traff)


def processLines():
    global currTime
   
    global lines
    global hopTraff
    global hopNeighbors
    global flows
    global attackRunning

    #print "Lines",lines
    getRoutes()
    getTraffTypeCounts()

    getAttackRunning()
    #writeDataExists()
    #print str((currTime-startTime))+";"+ str(flows) + ";" + str(routes)+";"+str(attackRunning)
    #print "Lines",lines

    lines = []
    hopTraff= {}
    hopNeighbors = {}
    flows = {}

    attackRunning = "none"

def getRoutes():
    global hopTraff
    global routes
    global hopNeighbors

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

        if splitLine[0] not in ipHopDict:
            ipHopDict[splitLine[0]] = (splitLine[2],splitLine[1])
    routes = ipHopDict
    #print "hopNeighbors",hopNeighbors
    #print "ROUTES",routes
    sys.stdout.flush()
    
def getTraffTypeCounts():
    global lines

    
    global flows
    
    srcIP = ""
    dstIP = ""

    for line in lines:
        #split the line by comma
        splitLine = line.split(",")
        
        srcIP = splitLine[3]
        dstIP = splitLine[4]

        if srcIP == "":
            srcIP = splitLine[5]
        if dstIP == "":
            dstIP = splitLine[6]
        if srcIP != "" and dstIP != "":
            #if it's my traffic, keep it in a special spot: #breaking here. only see 224.0.0.x traffic
            if srcIP not in myIPs and dstIP not in myIPs: # seems to be avoiding all traffic related to ALL interface IPs. WILL OTHERS BREAK IF RAN AGAIN? WILL IT GET ANY TRAFFIC IF ITS SUPPOSED TO BE A "HOST?"
                flow = srcIP + "_" + dstIP #port?

                print flow##################################################

                hopsToSrc = "*"
                hopsToDst = "*"
                if srcIP in routes:
                    hopsToSrc = routes[srcIP][0]
                if dstIP in routes:
                    hopsToDst = routes[dstIP][0]
                    
                if (flow,splitLine[2]) not in flows:
                    flows[(flow,splitLine[2])] = (hopsToSrc,hopsToDst)
                
def getAttackRunning():
    global attackRunning
    global filePath
    attackRunning = commands.getoutput("cat " + filePath + "/attack.txt")
    if "No such file or directory" in attackRunning:
        attackRunning = "none"
     

while 1:
    line = sys.stdin.readline()

    currTime = int(line.split(",")[0].split(".")[0])
#        currTime=int(commands.getoutput("date +%s"))
    if currTime >= prevTime + 1:
#        print "CurrTime",currTime
        prevTime = currTime
	processLines()
    lines.append(line)
#        time.sleep(0) #sleep for a specified amount of time.
