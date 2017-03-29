#!/usr/bin/python
import time
import thread
import sys
import commands
import ast
import re
import networkx as nx
from netaddr import IPNetwork, IPAddress

nBeforeAttack = sys.argv[1]
mAfterAttack = sys.argv[2]
attackerFile = sys.argv[3] # Sould be in x_x_x_x format 
netmask = sys.argv[4]
attackNodeIP = attackerFile.replace(".","_")


#output: 
#1. fromHop
#2. toHop
#3. type
#4. distance
#5. passthrough
#10. srcSpoofed
#11. destSpoofed
#12. hopsToSpoofed
#14. hopsFromSpoofedToDest
#15. spoofedBetweenAttacker
#16. isDstBetweenSpoofedAndAttacker
#17. spoofedBetweenAttackergw
#18. isDstBetweenSpoofedAndAttackergw
#19. isAttackerBetweenSpoofedAndDst
#20. isAttackerBetweenSpoofedAndDstgw
#21. isSrcBetweenSpoofedAndDst
#22. isSrcBetweenSpoofedAndDstgw
#23. altPathWithoutAttacker
#24. duringLinkLost

G = nx.Graph()

attackName = "none"
attackerPathsSeen = {}
nonAttackerFiles = []
nonAttackerFlowsBeforeAttack = {}
nonAttackerFlowsDuringAttack = {}
nonAttackerFlowsAfterAttack = {}

nonAttackerLossDuringAttack = {}
nonAttackerLossAfterAttack = {}
nonAttackerRecoveryAfterAttack = {}
hopTraff = {}
instance = ""

passThroughsBefore = {}
routes = {}
routesPrev = {}
destIsSpoofed = "false"
srcIsSpoofed = "false"
hopsToSpoofed = 0
hopsFromSpoofedToDest = -1
nonAttackerRoutes = {}
attackerCloserToDestThanSpoofed = "false"
gateways = {}
#passThroughsDuring = {}
#passThroughsAfter = {}

#fromHop, toHop,#hopsDataTravels, traffType, PacketsSeenBeforeAttack
#attack, numPackets deviation during attack, passthrough, deviationAfterAttack 
#---pending---:
#recoverTime
#iDstSpoofed, isSrcAttacker, secondsUntilHit
target = open("/root/Desktop/test.txt", 'w')



def getAttackerPerspective():
    global attackerPathsSeen
    global nBeforeAttack
    global attackName
    global routes
    global gateways
    global attackNodeIP
    global attackerFile
    global G
    global target
    statesNBeforeAttack = []  
    #need to open the attacker files first
    attackerFile = open(attackerFile + '.capture')
    lines = attackerFile.readlines()[2:-1]
    lineNum = 0


    #now populate the attacker's gateways:

    for line in lines:
        lineNum = lineNum +1
        time = int(ast.literal_eval(line.split(";")[0]))
        flows = ast.literal_eval(line.split(";")[1])
        target.write("FLOWS: "+str(flows))
        routesPrev = routes
        routes = ast.literal_eval(line.split(";")[2]) # NO ROUTES BEING GIVEN! ---------- SHOULD BE TAKEN CARE OF BY MAKING ALL ROUTERS
        attackRunning = line.split(";")[3]
        target.write("\n"+str(routes)+"\n")

        #get all network bypass n before attack from flows:
        if attackRunning.startswith("no") and lineNum < len(lines):
            if len(statesNBeforeAttack) > int(nBeforeAttack):
                statesNBeforeAttack.pop()
            statesNBeforeAttack.append(flows)
        else :
            routes = routesPrev
            attackName = attackRunning.strip()
            for sRoute in routes:
                if (attackNodeIP,sRoute) not in gateways:
                    gateways[(attackNodeIP,sRoute)] = routes[sRoute][1]
                if routes[sRoute][1] != "0.0.0.0":
                    G.add_edge(attackNodeIP,routes[sRoute][1])
        if lineNum == len(lines):
            attackName = "down"
            break
        
    #get the union of all paths seen
    for allFlows in statesNBeforeAttack:
        for flow in allFlows:
            #convert the traff parameter to either tcp,udp or unk
            tmpFlow = flow
            if "udp" in tmpFlow[1]:
                tmpFlow = (tmpFlow[0],"UDP")
            elif "tcp" in tmpFlow[1]:
                tmpFlow = (tmpFlow[0],"TCP")
            if tmpFlow not in attackerPathsSeen:
                attackerPathsSeen[tmpFlow] = allFlows[flow]
            #else:
                #print "old",flow

def getNonAttackerPerspective(): #next open the non-attackers files and fill out parameters
    global numAttackLines
    global attackerPathsSeen
    global nBeforeAttack
    global mAfterAttack
    global nonAttackerFiles
    global nonAttackerFlowsBeforeAttack
    global nonAttackerFlowsDuringAttack
    global nonAttackerFlowsAfterAttack
    global nonAttackerRoutes
    global attackName
    global G
    
    sysNonAttackerFiles = commands.getoutput("ls *.mgencapture")
    
    for sysNonAttackerFile in sysNonAttackerFiles.split("\n"):
        state = "before"
        nodeFromFilename = sysNonAttackerFile.split(".")[0].replace("_",".")
        nonAttackerFiles.append(sysNonAttackerFile)
        nonAttackerFile = open(sysNonAttackerFile)
        fileStatesNBeforeAttack = []
        fileStatesDuringAttack = []
        fileStatesMAfterAttack = []
        numAttackLines = 0
        lines = nonAttackerFile.readlines()[2:-1] #exclude last line (may be corrupt).

        for line in lines:
            elements = len(line.split(";"))
            if elements < 8:
                continue
            time = int(ast.literal_eval(line.split(";")[0]))
            flows = ast.literal_eval(line.split(";")[1])

            attackRunning = line.split(";")[6]
                
            if state == "before":          
                if attackRunning.startswith("no"):
					
                    #populate routes and gateways:
                    nonAttackerRoutesSingle = ast.literal_eval(line.split(";")[7])
                    
                    for sRoute in nonAttackerRoutesSingle:
                        nonAttackerRoutes[(nodeFromFilename,sRoute)] = nonAttackerRoutesSingle[sRoute][0] 

                        for sRoute in nonAttackerRoutesSingle:
                            gateways[(nodeFromFilename,sRoute)] = nonAttackerRoutesSingle[sRoute][1]
                            if nonAttackerRoutesSingle[sRoute][1] != "0.0.0.0":
                                G.add_edge(nodeFromFilename,nonAttackerRoutesSingle[sRoute][1])
                                
                    if len(fileStatesNBeforeAttack) >= int(nBeforeAttack):
                        fileStatesNBeforeAttack.pop()
                    fileStatesNBeforeAttack.append(flows)

                else :
                    state = "during"
                    
                    #get the union of all paths seen
                    for allFlows in fileStatesNBeforeAttack:
                        for flow in allFlows:
                            if flow not in nonAttackerFlowsBeforeAttack:
                                nonAttackerFlowsBeforeAttack[flow] = allFlows[flow]
                            else:
                                nonAttackerFlowsBeforeAttack[flow] = (allFlows[flow][0]+nonAttackerFlowsBeforeAttack[flow][0],allFlows[flow][1]+nonAttackerFlowsBeforeAttack[flow][1],allFlows[flow][2]+nonAttackerFlowsBeforeAttack[flow][2],allFlows[flow][3]+nonAttackerFlowsBeforeAttack[flow][3],allFlows[flow][4])
            if state == "during":
                #now I need to calculate which I'm missing every second?
                if not attackRunning.startswith("no"):
                    fileStatesDuringAttack.append(flows)
                    #have to make correspond with file, because some are different
                    numAttackLines+=1
                else :
                    state = "after"
                    #get the union of all paths seen
                    for allFlows in fileStatesDuringAttack:
                        for flow in allFlows:
                            if flow not in nonAttackerFlowsDuringAttack:
                                nonAttackerFlowsDuringAttack[flow] = (allFlows[flow][0],allFlows[flow][1],allFlows[flow][2],allFlows[flow][3],allFlows[flow][4],numAttackLines)
                            else:
                                nonAttackerFlowsDuringAttack[flow] = (allFlows[flow][0]+nonAttackerFlowsDuringAttack[flow][0],allFlows[flow][1]+nonAttackerFlowsDuringAttack[flow][1],allFlows[flow][2]+nonAttackerFlowsDuringAttack[flow][2],allFlows[flow][3]+nonAttackerFlowsDuringAttack[flow][3],allFlows[flow][4],numAttackLines)
            if state == "after":
                
                #now I need to calculate which I'm missing every second?
                #get all network bypass n before attack from flows:
                if attackRunning.startswith("no"):
                    if len(fileStatesMAfterAttack) < int(mAfterAttack):
                        fileStatesMAfterAttack.append(flows)
                    if len(fileStatesMAfterAttack) == int(mAfterAttack): 
                        state = "done" #the last line is ignored because of this
                        #get the union of all paths seen
                        for allFlows in fileStatesMAfterAttack:
                            for flow in allFlows:
                                if flow not in nonAttackerFlowsAfterAttack:
                                    nonAttackerFlowsAfterAttack[flow] = allFlows[flow]
                                else:
                                    nonAttackerFlowsAfterAttack[flow] = (allFlows[flow][0]+nonAttackerFlowsAfterAttack[flow][0],allFlows[flow][1]+nonAttackerFlowsAfterAttack[flow][1],allFlows[flow][2]+nonAttackerFlowsAfterAttack[flow][2],allFlows[flow][3]+nonAttackerFlowsAfterAttack[flow][3],allFlows[flow][4])

def calcBeforeAttackAvgs():   
    global nonAttackerFlowsBeforeAttack

    for flow in nonAttackerFlowsBeforeAttack:
        nonAttackerFlowsBeforeAttack[flow] = (nonAttackerFlowsBeforeAttack[flow][0]/float(nBeforeAttack),nonAttackerFlowsBeforeAttack[flow][1]/float(nBeforeAttack),nonAttackerFlowsBeforeAttack[flow][2]/float(nBeforeAttack),nonAttackerFlowsBeforeAttack[flow][3]/float(nBeforeAttack),nonAttackerFlowsBeforeAttack[flow][4])
        
def calcDuringAttackAvgs():
    global numAttackLines
    global nonAttackerFlowsDuringAttack
    
    for flow in nonAttackerFlowsDuringAttack:
        #div = nonAttackerFlowsDuringAttack[flow][5]
        div = 60.0
        nonAttackerFlowsDuringAttack[flow] = (nonAttackerFlowsDuringAttack[flow][0]/float(div),nonAttackerFlowsDuringAttack[flow][1]/float(div),nonAttackerFlowsDuringAttack[flow][2]/float(div),nonAttackerFlowsDuringAttack[flow][3]/float(div),nonAttackerFlowsDuringAttack[flow][4],div)
    
def calcAfterAttackAvgs():
    global nonAttackerFlowsAfterAttack

    for flow in nonAttackerFlowsAfterAttack:
        nonAttackerFlowsAfterAttack[flow] = (nonAttackerFlowsAfterAttack[flow][0]/float(mAfterAttack),nonAttackerFlowsAfterAttack[flow][1]/float(mAfterAttack),nonAttackerFlowsAfterAttack[flow][2]/float(mAfterAttack),nonAttackerFlowsAfterAttack[flow][3]/float(mAfterAttack),nonAttackerFlowsAfterAttack[flow][4])

    
def getNonAttackerLossDuringAttack():
    #during - before
    #first get avgs of all
    global numAttackLines
    global nonAttackerFlowsBeforeAttack
    global nonAttackerFlowsDuringAttack
    global nonAttackerLossDuringAttack
    #measure diffs in the ones I know
    for flow in nonAttackerFlowsBeforeAttack:
        if flow in nonAttackerFlowsDuringAttack: 
            nonAttackerLossDuringAttack[flow] = (nonAttackerFlowsBeforeAttack[flow][0]-nonAttackerFlowsDuringAttack[flow][0],nonAttackerFlowsBeforeAttack[flow][1]-nonAttackerFlowsDuringAttack[flow][1],nonAttackerFlowsBeforeAttack[flow][2]-nonAttackerFlowsDuringAttack[flow][2],nonAttackerFlowsBeforeAttack[flow][3]-nonAttackerFlowsDuringAttack[flow][3],nonAttackerFlowsBeforeAttack[flow][4])
        else:
            nonAttackerLossDuringAttack[flow] = nonAttackerFlowsBeforeAttack[flow] 

def getNonAttackerLossAfterAttack():
    #after - before
    #first get avgs of all
    global nonAttackerFlowsBeforeAttack
    global nonAttackerFlowsDuringAttack
    global nonAttackerFlowsAfterAttack
    global nonAttackerLossDuringAttack
    global nonAttackerLossAfterAttack
    global nonAttackerRecoveryAfterAttack
    #see if the ones that disappeared, reappear 
    for flow in nonAttackerFlowsBeforeAttack:
        if flow in nonAttackerFlowsAfterAttack:
            nonAttackerLossAfterAttack[flow] = (nonAttackerFlowsBeforeAttack[flow][0]-nonAttackerFlowsAfterAttack[flow][0],nonAttackerFlowsBeforeAttack[flow][1]-nonAttackerFlowsAfterAttack[flow][1],nonAttackerFlowsBeforeAttack[flow][2]-nonAttackerFlowsAfterAttack[flow][2],nonAttackerFlowsBeforeAttack[flow][3]-nonAttackerFlowsAfterAttack[flow][3],nonAttackerFlowsBeforeAttack[flow][4])
        else:
            nonAttackerLossAfterAttack[flow] = nonAttackerFlowsBeforeAttack[flow]
    
def calcPassThroughs():
    global nonAttackerFlowsBeforeAttack
    global attackerPathsSeen
    global passThroughsBefore
    global target
    for flow in nonAttackerFlowsBeforeAttack:
        fromHop = "*"
        toHop = "*"
        toIP = flow[0].split("_")[1]
        fromIP = flow[0].split("_")[0]
        ipToRange = IPNetwork(toIP + "/" + netmask)
        ipFromRange = IPNetwork(fromIP + "/" + netmask)
        
        target.write("nonattacker flows: "+str(nonAttackerFlowsBeforeAttack))
        
        #if fromIP not in routes and IPAddress(fromIP) in ipFromRange:
         #   fromHop = ipToRange[0]  #Not changing for wired scenarios------------------------------------------------
        if fromIP in routes:
            fromHop = routes[fromIP][0]
        target.write("\n toip:" +toIP + "\n") 
        if toIP not in routes and IPAddress(toIP) in ipToRange:
            toIP = ipFromRange[0]
        if toIP in routes:
            toHop = routes[toIP][0]
        target.write("\n fromhop: "+ fromHop +" tohop: " + toHop + "\n" + "routes: " + str(routes))    
        if (flow[0],flow[1]) in attackerPathsSeen: # CHECK ALL THREE IN TEST.TXT!---------------------
            passThroughsBefore[(flow[0],flow[1])] = ("true",flow[0].split("_")[0],fromHop,flow[0].split("_")[1],toHop)
        else:
            passThroughsBefore[(flow[0],flow[1])] = ("false",flow[0].split("_")[0],fromHop,flow[0].split("_")[1],toHop)
       
def buildHopTraff():
    global nonAttackerFlowsBeforeAttack
    global nonAttackerFlowsDuringAttack
    global nonAttackerFlowsAfterAttack
    global nonAttackerLossDuringAttack
    global nonAttackerLossAfterAttack
    global nonAttackerRecoveryAfterAttack
    global passThroughsBefore
    global attackName
    global attackNodeIP
    global instance
    global destIsSpoofed
    global srcIsSpoofed
    global hopsToSpoofed
    global hopsFromSpoofedToDest
    global attackerCloserToDestThanSpoofed
    #FromHop,ToHop,Type,Dist,Passthrough, Before,During,After,AttackName - don't include *s

    for flow in nonAttackerFlowsBeforeAttack:
        fromHop = passThroughsBefore[(flow[0],flow[1])][2]
        #target.write("\n passthroughbefore" + str(passThroughsBefore) +"\n nonattackerflowsbeforeattack: "+ str(nonAttackerFlowsBeforeAttack) + "\n flow 1 and 2 " + str(flow[0])+"---"+str(flow[1]) +"\n")
        
        toHop = passThroughsBefore[(flow[0],flow[1])][4]

        fromIP = flow[0].split("_")[0]
        toIP = flow[0].split("_")[1] #may contain x.x.x.n format
        ipRange = IPNetwork(toIP + "/" + netmask)
        
        #see if ip must be modified (nonAttackerRoutes may contain x.x.x.0 format if wired)
        if IPAddress(toIP) in ipRange and (fromIP, toIP) not in nonAttackerRoutes:
			toIP = ipRange[0]
		
		#check again with new ip value
        if (fromIP, toIP) in nonAttackerRoutes: 
            dist = nonAttackerRoutes[fromIP,toIP] 
        else: 
            dist = "*"

        target.write("nonattackroutes: "+ str(nonAttackerRoutes)+"\n"+"RESULTS: " + str(toHop) + "---" + str(fromHop) +"---" + str(dist))
        if not fromHop == "*" and not toHop == "*" and not dist == "*": 

            type = flow[1]
            if type == "TCP" or type == "UDP":

                tmpPassthrough = bBetweenAandC(flow[0].split("_")[0],attackNodeIP,flow[0].split("_")[1])
                passThrough = passThroughsBefore[(flow[0],flow[1])][0]
                  
                beforeDelay = nonAttackerFlowsBeforeAttack[flow][0]
                beforeMissed = nonAttackerFlowsBeforeAttack[flow][1]
                beforeOOO = nonAttackerFlowsBeforeAttack[flow][2]
                beforeNumPackets = nonAttackerFlowsBeforeAttack[flow][3]
        
                duringDelay = nonAttackerLossDuringAttack[flow][0]
                duringMissed = nonAttackerLossDuringAttack[flow][1]
                duringOOO = nonAttackerLossDuringAttack[flow][2]
                duringNumPackets = nonAttackerLossDuringAttack[flow][3]
                
                afterDelay = nonAttackerLossAfterAttack[flow][0]
                afterMissed = nonAttackerLossAfterAttack[flow][1]
                afterOOO = nonAttackerLossAfterAttack[flow][2]
                afterNumPackets = nonAttackerLossAfterAttack[flow][3]

                srcIsSpoofed = "false"
                destIsSpoofed = "false"
                hopsToSpoofed = 0
                hopsFromSpoofedToDest = -1
                attackerCloserToDestThanSpoofed = "false"
                tempOut = ""
                isSpoofedBetweenAttacker = "false"
                isSpoofedBetweenAttackergw = "false"
                isDstBetweenSpoofedAndAttacker = "false"
                isDstBetweenSpoofedAndAttackergw = "false"
                isAttackerBetweenSpoofedAndDst = "false"
                isAttackerBetweenSpoofedAndDstgw = "false"
                isSrcBetweenSpoofedAndDst = "false"
                isSrcBetweenSpoofedAndDstgw = "false"
                if "spoof" in attackName:
                    if flow[0].split("_")[1] == attackName.split("_")[1]:
                        destIsSpoofed = "true"
                        
                    if flow[0].split("_")[0] == attackName.split("_")[1]:
                        srcIsSpoofed = "true"
                        
                    if attackName.split("_")[1] in routes:
                        hopsToSpoofed = routes[attackName.split("_")[1]][0]
                    
                    if destIsSpoofed == "true":
                        hopsFromSpoofedToDest = 0
                    elif (attackName.split("_")[1],flow[0].split("_")[1]) in nonAttackerRoutes:
                        hopsFromSpoofedToDest = nonAttackerRoutes[(attackName.split("_")[1],flow[0].split("_")[1])][0]
                    
                    if toHop < hopsFromSpoofedToDest or hopsFromSpoofedToDest == -1:
                        attackerCloserToDestThanSpoofed = "true"
                    tempOut = attackName.split("_")[1]  + flow[0].split("_")[1]
                   
                    #is spoofed between src and attacker 
                    isSpoofedBetweenAttacker = bBetweenAandC(flow[0].split("_")[0],attackName.split("_")[1],attackNodeIP)
                    isSpoofedBetweenAttackergw = gatewaybBetweenAandC(flow[0].split("_")[0],attackName.split("_")[1],attackNodeIP)
                    
                    #is dst between spoofed and attacker - dst,spoof,attack
                    isDstBetweenSpoofedAndAttacker = bBetweenAandC(flow[0].split("_")[1],attackName.split("_")[1],attackNodeIP)
                    isDstBetweenSpoofedAndAttackergw = gatewaybBetweenAandC(flow[0].split("_")[1],attackName.split("_")[1],attackNodeIP)
                    
                    isAttackerBetweenSpoofedAndDst = bBetweenAandC(attackName.split("_")[1],attackNodeIP,flow[0].split("_")[1])
                    isAttackerBetweenSpoofedAndDstgw = gatewaybBetweenAandC(attackName.split("_")[1],attackNodeIP,flow[0].split("_")[1])
                    
                    isSrcBetweenSpoofedAndDst = bBetweenAandC(attackName.split("_")[1],flow[0].split("_")[0],flow[0].split("_")[1])
                    isSrcBetweenSpoofedAndDstgw = gatewaybBetweenAandC(attackName.split("_")[1],flow[0].split("_")[0],flow[0].split("_")[1])
                 
                if int(duringNumPackets) > 25: #if a fifth of the packets are lost, count it as lost flow
                    duringLinkLost = "true"
                else: duringLinkLost = "false"
                if int(afterNumPackets) > 25:
                    afterLinkLost = "true"
                else: afterLinkLost = "false"

                instance += commands.getoutput("pwd").strip('\n')+","+attackNodeIP+","+str(flow[0])+","+str(fromHop)+","+str(toHop)+","+str(type)+","+str(dist)+","+str(tmpPassthrough)+","+str(beforeDelay)+","+str(beforeMissed)+","+str(beforeOOO)+","+str(beforeNumPackets)+","+str(duringDelay)+","+str(duringMissed)+","+str(duringOOO)+","+str(duringNumPackets)+","+str(afterDelay)+","+str(afterMissed)+","+str(afterOOO)+","+str(afterNumPackets)+","+str(srcIsSpoofed)+","+str(destIsSpoofed)+","+str(hopsToSpoofed)+","+str(duringLinkLost)+","+str(afterLinkLost)+","+str(attackName) +","+str(hopsFromSpoofedToDest)+ ","+str(attackerCloserToDestThanSpoofed)+","+str(isSpoofedBetweenAttacker)+","+str(isDstBetweenSpoofedAndAttacker)+","+str(isSpoofedBetweenAttackergw)+","+str(isDstBetweenSpoofedAndAttackergw)+","+str(isAttackerBetweenSpoofedAndDst)+","+str(isAttackerBetweenSpoofedAndDstgw)+","+str(isSrcBetweenSpoofedAndDst)+","+str(isSrcBetweenSpoofedAndDstgw)+","+str(hasAltPath(flow[0].split("_")[0],flow[0].split("_")[1],attackNodeIP))
                instance = instance.strip('\n')
                instance += '\n'
                
def bBetweenAandC(a,b,c):
    global gateways
    done = "false"
    mysrc = a
#    print a,b,c,"hop to ",mysrc,",",c
    if mysrc == b:
        return "true"
    while "true":
        if (mysrc,c) in gateways:
            mysrc = gateways[(mysrc,c)]
#            print "hop to ",mysrc,",",c
            if mysrc == "0.0.0.0":
                return "false"
            if mysrc == b:
                return "true"
        else: return "false"
        
def gatewaybBetweenAandC(a,b,c):
    global gateways
    done = "false"
    mysrc = a
#    print a,b,c,"hop to ",mysrc,",",c
    if mysrc == b or ((mysrc,b) in gateways and gateways[(mysrc,b)] == "0.0.0.0"):
        return "true"
    while "true":
        if (mysrc,c) in gateways:
            mysrc = gateways[(mysrc,c)]
#            print "hop to ",mysrc,",",c
            if mysrc == "0.0.0.0":
                return "false"
            if mysrc == b or ((mysrc,b) in gateways and gateways[(mysrc,b)] == "0.0.0.0"):
                return "true"
        else: return "false"


    
def hasAltPath(fromNode,toNode,nodeToRemove):
    return "true"
    global G

    if not nx.has_path(G,fromNode,toNode):
        return "false"
    temp = G.copy()
    temp.remove_node(nodeToRemove)
    if not nx.has_path(temp,fromNode,toNode):
        return "false"
    return "true"

getAttackerPerspective()
getNonAttackerPerspective()
calcBeforeAttackAvgs()
calcDuringAttackAvgs()
calcAfterAttackAvgs()
getNonAttackerLossDuringAttack()
getNonAttackerLossAfterAttack()

calcPassThroughs()
buildHopTraff()
target.close() 
print instance


