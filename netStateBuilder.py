#!/usr/bin/python
import time
import thread
import sys
import commands
import ast
import networkx as nx

nBeforeAttack = sys.argv[1]
mAfterAttack = sys.argv[2]
attackNodeNum = sys.argv[3]

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

attackNodeIP = ""

#fromHop, toHop,#hopsDataTravels, traffType, PacketsSeenBeforeAttack
#attack, numPackets deviation during attack, passthrough, deviationAfterAttack 
#---pending---:
#recoverTime
#iDstSpoofed, isSrcAttacker, secondsUntilHit


def getAttackerPerspective():
    global attackerPathsSeen
    global nBeforeAttack
    global attackName
    global routes
    global gateways
    global attackNodeIP
    global G
    
    statesNBeforeAttack = []  
    #need to open the attacker files first
    attackerFile = open('n'+attackNodeNum+'.capture')
    lines = attackerFile.readlines()[2:-1]
    lineNum = 0
    for line in lines:
        lineNum = lineNum +1
        time = int(ast.literal_eval(line.split(";")[0]))
        
        flows = ast.literal_eval(line.split(";")[1])
        routesPrev = routes
        routes = ast.literal_eval(line.split(";")[2])
        attackRunning = line.split(";")[3]
#        print "attackRunning: ",attackRunning
        #get all network bypass n before attack from flows:
        #print attackRunning
        if attackRunning.startswith("no") and lineNum < len(lines):
            if len(statesNBeforeAttack) > int(nBeforeAttack):
                #print "removing"
                statesNBeforeAttack.pop()
            statesNBeforeAttack.append(flows)
        else :
            routes = routesPrev
            attackName = attackRunning.strip()
            #now populate the attacker's gateways:
            attackNodeIP = "10.0.0." + attackNodeNum
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
        #print "allFlows",allFlows
        for flow in allFlows:
            #print "flow",flow
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
    #print "Paths", attackerPathsSeen,"len",len(attackerPathsSeen)

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
    global attackNodeNum
    global G
    
    sysNonAttackerFiles = commands.getoutput("ls *.mgencapture")
    allStatesNBeforeAttack = []
    
#TODO: Here get all routes    
    for sysNonAttackerFile in sysNonAttackerFiles.split("\n"):
        state = "before"
        nodeFromFilename = "10.0.0."+sysNonAttackerFile.split(".")[0].split("n")[1]
        nonAttackerFiles.append(sysNonAttackerFile)
        nonAttackerFile = open(sysNonAttackerFile)
        fileStatesNBeforeAttack = []
        fileStatesDuringAttack = []
        fileStatesMAfterAttack = []
        numAttackLines = 0
        lines = nonAttackerFile.readlines()[2:-1]

#            for g in gateways:
#                print g,gateways[g]

        for line in lines:
            #print "line:",line
            #print nonAttackerRoutes
            time = int(ast.literal_eval(line.split(";")[0]))
            flows = ast.literal_eval(line.split(";")[1])
            
            #print flows
            attackRunning = line.split(";")[6]
            #print "in nonAttacker, attackName",attackName
            #print "running",attackRunning
            #print "state",state
            #nonAttackerFlowsBeforeAttack = {}
            #nonAttackerFlowsDuringAttack = {}
            #nonAttackerFlowsAfterAttack = {}
                
            if state == "before":              
                #get all network bypass n before attack from flows:
                #print attackRunning
                if attackRunning.startswith("no"):
                    #populate routes and gateways:
                    #print line,nonAttackerRoutesSingle
                    nonAttackerRoutesSingle = ast.literal_eval(line.split(";")[7])
                    #print "here1"
                    for sRoute in nonAttackerRoutesSingle:
                        nonAttackerRoutes[(nodeFromFilename,sRoute)] = nonAttackerRoutesSingle[sRoute][0]
                        for sRoute in nonAttackerRoutesSingle:
                            gateways[(nodeFromFilename,sRoute)] = nonAttackerRoutesSingle[sRoute][1]
                            if nonAttackerRoutesSingle[sRoute][1] != "0.0.0.0":
                                G.add_edge(nodeFromFilename,nonAttackerRoutesSingle[sRoute][1])

                    #print "here2"
                    if len(fileStatesNBeforeAttack) >= int(nBeforeAttack):
                        #print "removing"
                        fileStatesNBeforeAttack.pop()
                    fileStatesNBeforeAttack.append(flows)
                    #print "here3"
                else :
                    state = "during"
                    
                    #get the union of all paths seen
                    for allFlows in fileStatesNBeforeAttack:
                        #print "allFlows",allFlows
                        for flow in allFlows:
                            #print "flow",flow,":",allFlows[flow]
                            if flow not in nonAttackerFlowsBeforeAttack:
                                nonAttackerFlowsBeforeAttack[flow] = allFlows[flow]
                            else:
                                #print "adding",flow,nonAttackerFlowsBeforeAttack[flow]
                                nonAttackerFlowsBeforeAttack[flow] = (allFlows[flow][0]+nonAttackerFlowsBeforeAttack[flow][0],allFlows[flow][1]+nonAttackerFlowsBeforeAttack[flow][1],allFlows[flow][2]+nonAttackerFlowsBeforeAttack[flow][2],allFlows[flow][3]+nonAttackerFlowsBeforeAttack[flow][3],allFlows[flow][4])
                                #print "now",nonAttackerFlows[flow]
                    #print "Before", nonAttackerFlowsBeforeAttack,"len",len(nonAttackerFlowsBeforeAttack),sysNonAttackerFile,numBeforeLines
                    #print "First LINe for During: ", line
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
                        #print "allFlows",allFlows
                        for flow in allFlows:
                            #print "during","flow",flow,":",allFlows[flow]
                            if flow not in nonAttackerFlowsDuringAttack:
                                nonAttackerFlowsDuringAttack[flow] = (allFlows[flow][0],allFlows[flow][1],allFlows[flow][2],allFlows[flow][3],allFlows[flow][4],numAttackLines)
                            else:
                                nonAttackerFlowsDuringAttack[flow] = (allFlows[flow][0]+nonAttackerFlowsDuringAttack[flow][0],allFlows[flow][1]+nonAttackerFlowsDuringAttack[flow][1],allFlows[flow][2]+nonAttackerFlowsDuringAttack[flow][2],allFlows[flow][3]+nonAttackerFlowsDuringAttack[flow][3],allFlows[flow][4],numAttackLines)
                                #print "now",nonAttackerFlows[flow]
                    #for flow in nonAttackerFlowsDuringAttack:
                    #    print "During", flow,nonAttackerFlowsDuringAttack[flow],"len",len(nonAttackerFlowsDuringAttack[flow]),sysNonAttackerFile,numAttackLines
                    #print "First LINe for After: ", line
            if state == "after":
                
                #now I need to calculate which I'm missing every second?
                #get all network bypass n before attack from flows:
                #print attackRunning
                if attackRunning.startswith("no"):
                    if len(fileStatesMAfterAttack) < int(mAfterAttack):
                        fileStatesMAfterAttack.append(flows)
                    if len(fileStatesMAfterAttack) == int(mAfterAttack): 
                        state = "done" #the last line is ignored because of this
                        #get the union of all paths seen
                        for allFlows in fileStatesMAfterAttack:
                            #print "allFlows",allFlows
                            for flow in allFlows:
                                #print "flow",flow,":",allFlows[flow]
                                if flow not in nonAttackerFlowsAfterAttack:
                                    nonAttackerFlowsAfterAttack[flow] = allFlows[flow]
                                else:
                                    #print "adding",flow,nonAttackerFlowsAfterAttack[flow]
                                    nonAttackerFlowsAfterAttack[flow] = (allFlows[flow][0]+nonAttackerFlowsAfterAttack[flow][0],allFlows[flow][1]+nonAttackerFlowsAfterAttack[flow][1],allFlows[flow][2]+nonAttackerFlowsAfterAttack[flow][2],allFlows[flow][3]+nonAttackerFlowsAfterAttack[flow][3],allFlows[flow][4])
                                    #print "now",nonAttackerFlows[flow]
                        #print "After", nonAttackerFlowsAfterAttack,"len",len(nonAttackerFlowsAfterAttack),sysNonAttackerFile,numAfterLines
#        if numAttackLines < 10:
#            print "!!!!ERROR",attackNodeNum,attackName,sysNonAttackerFile
        
def calcBeforeAttackAvgs():   
    global nonAttackerFlowsBeforeAttack

    for flow in nonAttackerFlowsBeforeAttack:
        #print nonAttackerFlowsBeforeAttack[flow],"div",nBeforeAttack
        nonAttackerFlowsBeforeAttack[flow] = (nonAttackerFlowsBeforeAttack[flow][0]/float(nBeforeAttack),nonAttackerFlowsBeforeAttack[flow][1]/float(nBeforeAttack),nonAttackerFlowsBeforeAttack[flow][2]/float(nBeforeAttack),nonAttackerFlowsBeforeAttack[flow][3]/float(nBeforeAttack),nonAttackerFlowsBeforeAttack[flow][4])
#        print nonAttackerFlowsBeforeAttack[flow],"div",nBeforeAttack
    
    
def calcDuringAttackAvgs():
    global numAttackLines
    global nonAttackerFlowsDuringAttack
    
    for flow in nonAttackerFlowsDuringAttack:
  #      print "BEFORE:::::::::::::::::::"
   #     print flow,nonAttackerFlowsDuringAttack[flow],"div",nonAttackerFlowsDuringAttack[flow][5]
        #div = nonAttackerFlowsDuringAttack[flow][5]
        div = 60.0
 #       print "div",div
        nonAttackerFlowsDuringAttack[flow] = (nonAttackerFlowsDuringAttack[flow][0]/float(div),nonAttackerFlowsDuringAttack[flow][1]/float(div),nonAttackerFlowsDuringAttack[flow][2]/float(div),nonAttackerFlowsDuringAttack[flow][3]/float(div),nonAttackerFlowsDuringAttack[flow][4],div)
#        print "AFTER:::::::::::::::::::"
        #print flow,nonAttackerFlowsDuringAttack[flow],"div",nonAttackerFlowsDuringAttack[flow][5]
    
def calcAfterAttackAvgs():
    global nonAttackerFlowsAfterAttack

    for flow in nonAttackerFlowsAfterAttack:
        #print nonAttackerFlowsBeforeAttack[flow],"div",nBeforeAttack
        nonAttackerFlowsAfterAttack[flow] = (nonAttackerFlowsAfterAttack[flow][0]/float(mAfterAttack),nonAttackerFlowsAfterAttack[flow][1]/float(mAfterAttack),nonAttackerFlowsAfterAttack[flow][2]/float(mAfterAttack),nonAttackerFlowsAfterAttack[flow][3]/float(mAfterAttack),nonAttackerFlowsAfterAttack[flow][4])
#        print nonAttackerFlowsAfterAttack[flow],"div",nBeforeAttack
    
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
    # "before:\n"
    #for flow in nonAttackerFlowsBeforeAttack:
    #    print flow
    #print "during:\n"
    #for flow in nonAttackerFlowsDuringAttack:
    #    print flow
    #for flow in nonAttackerLossDuringAttack:
    #    print "diff",flow,nonAttackerLossDuringAttack[flow]
    

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
#    for flow in nonAttackerLossAfterAttack:
#        print "diff",flow,nonAttackerLossAfterAttack[flow]
    
def calcPassThroughs():
    global nonAttackerFlowsBeforeAttack
    global attackerPathsSeen
    global passThroughsBefore
    
    for flow in nonAttackerFlowsBeforeAttack:
        fromHop = "*"
        toHop = "*"
        if flow[0].split("_")[0] in routes:
            fromHop = routes[flow[0].split("_")[0]][0]
        if flow[0].split("_")[1] in routes:
            toHop = routes[flow[0].split("_")[1]][0]

        if (flow[0],flow[1]) in attackerPathsSeen: 
            passThroughsBefore[(flow[0],flow[1])] = ("true",flow[0].split("_")[0],fromHop,flow[0].split("_")[1],toHop)
        else:
            passThroughsBefore[(flow[0],flow[1])] = ("false",flow[0].split("_")[0],fromHop,flow[0].split("_")[1],toHop)
#    for a in passThroughsBefore:
#        print passThroughsBefore[a]
       
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
        toHop = passThroughsBefore[(flow[0],flow[1])][4]
        if (flow[0].split("_")[0],flow[0].split("_")[1]) not in nonAttackerRoutes:
            dist = "*"
        else: dist =nonAttackerRoutes[flow[0].split("_")[0],flow[0].split("_")[1]]

        if not fromHop == "*" and not toHop == "*" and not dist == "*":
            type = flow[1]
            if type == "TCP" or type == "UDP":
                #print "checking passthrough",flow[0].split("_")[0],attackNodeIP,flow[0].split("_")[1]
                tmpPassthrough = bBetweenAandC(flow[0].split("_")[0],attackNodeIP,flow[0].split("_")[1])
                #print tmpPassthrough
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
                        
                        #print "true",flow[0].split("_")[1],attackName.split("_")[1]
                                       
                    if flow[0].split("_")[0] == attackName.split("_")[1]:
                        srcIsSpoofed = "true"
                        
                        #print "true",flow[0].split("_")[0],attackName.split("_")[1]
                    if attackName.split("_")[1] in routes:
                        hopsToSpoofed = routes[attackName.split("_")[1]][0]
                    
                    if destIsSpoofed == "true":
                        hopsFromSpoofedToDest = 0
                    elif (attackName.split("_")[1],flow[0].split("_")[1]) in nonAttackerRoutes:
                        hopsFromSpoofedToDest = nonAttackerRoutes[(attackName.split("_")[1],flow[0].split("_")[1])][0]
                    
                    if toHop < hopsFromSpoofedToDest or hopsFromSpoofedToDest == -1:
                        attackerCloserToDestThanSpoofed = "true"
                    tempOut = attackName.split("_")[1]  + flow[0].split("_")[1]
                    #TODO: now get the number of hops from the spoofed to the destination
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
#                    print isDstBetweenSpoofedAndAttacker
#                print flow[0].split("_")[0],attackNodeIP,flow[0].split("_")[1]
                 
                if int(duringNumPackets) > 25: #if a fifth of the packets are lost, count it as lost flow
                    duringLinkLost = "true"
                else: duringLinkLost = "false"
                if int(afterNumPackets) > 25:
                    afterLinkLost = "true"
                else: afterLinkLost = "false"
                #print duringNumPackets
                #TODO: add the run name to each line:
#                instance += commands.getoutput("pwd").strip('\n')+","+str(attackNodeNum)+","+str(flow[0])+","+str(fromHop)+","+str(toHop)+","+str(type)+","+str(dist)+","+str(tmpPassthrough)+","+str(beforeDelay)+","+str(beforeMissed)+","+str(beforeOOO)+","+str(beforeNumPackets)+","+str(duringDelay)+","+str(duringMissed)+","+str(duringOOO)+","+str(duringNumPackets)+","+str(afterDelay)+","+str(afterMissed)+","+str(afterOOO)+","+str(afterNumPackets)+","+str(srcIsSpoofed)+","+str(destIsSpoofed)+","+str(hopsToSpoofed)+","+str(duringLinkLost)+","+str(afterLinkLost)+","+str(attackName) +","+str(hopsFromSpoofedToDest)+ ","+str(attackerCloserToDestThanSpoofed)+","+str(isSpoofedBetweenAttacker)+","+str(isDstBetweenSpoofedAndAttacker)+","+str(isSpoofedBetweenAttackergw)+","+str(isDstBetweenSpoofedAndAttackergw)+","+str(isAttackerBetweenSpoofedAndDst)+","+str(isAttackerBetweenSpoofedAndDstgw)+","+str(isSrcBetweenSpoofedAndDst)+","+str(isSrcBetweenSpoofedAndDstgw)+","+str(hasAltPath(flow[0].split("_")[0],flow[0].split("_")[1],attackNodeIP))
                instance += commands.getoutput("pwd").strip('\n')+","+str(attackNodeNum)+","+str(flow[0])+","+str(fromHop)+","+str(toHop)+","+str(type)+","+str(dist)+","+str(tmpPassthrough)+","+str(beforeDelay)+","+str(beforeMissed)+","+str(beforeOOO)+","+str(beforeNumPackets)+","+str(duringDelay)+","+str(duringMissed)+","+str(duringOOO)+","+str(duringNumPackets)+","+str(afterDelay)+","+str(afterMissed)+","+str(afterOOO)+","+str(afterNumPackets)+","+str(srcIsSpoofed)+","+str(destIsSpoofed)+","+str(hopsToSpoofed)+","+str(duringLinkLost)+","+str(afterLinkLost)+","+str(attackName) +","+str(hopsFromSpoofedToDest)+ ","+str(attackerCloserToDestThanSpoofed)+","+str(isSpoofedBetweenAttacker)+","+str(isDstBetweenSpoofedAndAttacker)+","+str(isSpoofedBetweenAttackergw)+","+str(isDstBetweenSpoofedAndAttackergw)+","+str(isAttackerBetweenSpoofedAndDst)+","+str(isAttackerBetweenSpoofedAndDstgw)+","+str(isSrcBetweenSpoofedAndDst)+","+str(isSrcBetweenSpoofedAndDstgw)+","+str(hasAltPath(flow[0].split("_")[0],flow[0].split("_")[1],attackNodeIP))
                instance = instance.strip('\n')
                instance += '\n'
                #.append((fromHop,toHop,type,dist,passThrough,beforeDelay,beforeMissed,beforeOOO,beforeNumPackets,duringDelay,duringMissed,duringOOO,duringNumPackets,afterDelay,afterMissed,afterOOO,afterNumPackets,attackName))
                #instance += str(flow[0])+","+str(fromHop)+","+str(toHop)+","+str(type)+","+str(dist)+","+str(passThrough)+","+str(beforeNumPackets)+","+str(duringNumPackets)+","+str(afterNumPackets) +"\n"
            #print "instance",instance

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
    global G

    if not nx.has_path(G,fromNode,toNode):
        return "false"
    temp = G.copy()
    temp.remove_node(nodeToRemove)
    if not nx.has_path(temp,fromNode,toNode):
        return "false"
    return "true"
    
getAttackerPerspective()
#print routes
getNonAttackerPerspective()
calcBeforeAttackAvgs()
calcDuringAttackAvgs()
calcAfterAttackAvgs()
getNonAttackerLossDuringAttack()
getNonAttackerLossAfterAttack()

calcPassThroughs()
buildHopTraff()

print instance

#print "AttPaths:",attackerPathsSeen
#print "nonAttBefore",nonAttackerFlowsBeforeAttack
#print "passThroughs",passThroughsBefore

 
