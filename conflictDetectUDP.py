#!/usr/bin/python
import time
import thread
import sys
import commands
import ast

inputFileName = sys.argv[1]

arffFile = open(inputFileName)

conflictConfigs = {}

lines = arffFile.readlines()[38:]

uniques = {}
lineNum=38
for line in lines:
    lineNum+=1
    #print "processing line: ",lineNum,line
    #if lineNum > 49:
#        break
    if not line.strip():
        continue
    params = line.split(",")
#    print line
    #need from,to,type,dist,passthrough,srcIsSpoofed,destIsSpoofed,duringLinkLost,attackName
    #2,3,4,5,6,19,20,21,22,23
    #print "len",len(params),"line",line
    path = params[0].split("/")
    path = path[len(path)-1]

    protocol = path.split("_")[7]
    scenFile = path.split("_")[8]
    if scenFile == "conn":
        scenFile = "conn_grid"
    elif scenFile == "two":
        scenFile = "two_centroidsCoords"

    attackNodeNum = params[1]
    fromHop = params[3]
    toHop = params[4]
    type = params[5]
    dist = params[6]
    passThrough = params[7]
    srcIsSpoofed = params[20]
    destIsSpoofed = params[21]
    hopsToSpoofed = params[22]
    duringLinkLost = params[23]

#    afterLinkLost = params[22]
    attackName = params[25]
    hopsFromSpoofedToDest = params[27]#26
    spoofedBetweenAttacker = params[28]#27
    isDstBetweenSpoofedAndAttacker = params[29]
    spoofedBetweenAttackergw = params[30]#27
    isDstBetweenSpoofedAndAttackergw = params[31]
    isAttackerBetweenSpoofedAndDst = params[32]
    isAttackerBetweenSpoofedAndDstgw = params[33] 
    isSrcBetweenSpoofedAndDst = params[34]
    isSrcBetweenSpoofedAndDstgw = params[35] 
    altPathWithoutAttacker = params[36]
    if "spoof" in attackName:
             attackName = "spoofingAttack"+attackName.split(".")[3].strip()+"_sh" 
    else:
        attackName = "forwardingAttack_sh"
    configName = attackNodeNum+"_60_60_"+attackName+"_jaime_scen_"+protocol+"_"+scenFile+"_txt"
    isForwarding = "no"
    if "forwarding" in attackName:
        isForwarding = "yes"
    if type != "TCP":
        if(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,hopsToSpoofed,isForwarding,hopsFromSpoofedToDest,spoofedBetweenAttacker,isDstBetweenSpoofedAndAttacker,spoofedBetweenAttackergw,isDstBetweenSpoofedAndAttackergw,isAttackerBetweenSpoofedAndDst,isAttackerBetweenSpoofedAndDstgw,isSrcBetweenSpoofedAndDst,isSrcBetweenSpoofedAndDstgw,altPathWithoutAttacker) not in uniques:
            uniques[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,hopsToSpoofed,isForwarding,hopsFromSpoofedToDest,spoofedBetweenAttacker,isDstBetweenSpoofedAndAttacker,spoofedBetweenAttackergw,isDstBetweenSpoofedAndAttackergw,isAttackerBetweenSpoofedAndDst,isAttackerBetweenSpoofedAndDstgw,isSrcBetweenSpoofedAndDst,isSrcBetweenSpoofedAndDstgw,altPathWithoutAttacker)] = [duringLinkLost]
            
            conflictConfigs[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,hopsToSpoofed,isForwarding,hopsFromSpoofedToDest,spoofedBetweenAttacker,isDstBetweenSpoofedAndAttacker,spoofedBetweenAttackergw,isDstBetweenSpoofedAndAttackergw,isAttackerBetweenSpoofedAndDst,isAttackerBetweenSpoofedAndDstgw,isSrcBetweenSpoofedAndDst,isSrcBetweenSpoofedAndDstgw,altPathWithoutAttacker)] = [(configName,duringLinkLost)]
            #print "uniques size",len(uniques),"conflicts size",len(conflictConfigs) 
            #now check if it's the same value:
        else:
            if duringLinkLost not in uniques[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,hopsToSpoofed,isForwarding,hopsFromSpoofedToDest,spoofedBetweenAttacker,isDstBetweenSpoofedAndAttacker,spoofedBetweenAttackergw,isDstBetweenSpoofedAndAttackergw,isAttackerBetweenSpoofedAndDst,isAttackerBetweenSpoofedAndDstgw,isSrcBetweenSpoofedAndDst,isSrcBetweenSpoofedAndDstgw,altPathWithoutAttacker)]:
    #           print "uniques",uniques
    #           print "appending line:",lineNum,"vals:", fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,duringLinkLost
                uniques[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,hopsToSpoofed,isForwarding,hopsFromSpoofedToDest,spoofedBetweenAttacker,isDstBetweenSpoofedAndAttacker,spoofedBetweenAttackergw,isDstBetweenSpoofedAndAttackergw,isAttackerBetweenSpoofedAndDst,isAttackerBetweenSpoofedAndDstgw,isSrcBetweenSpoofedAndDst,isSrcBetweenSpoofedAndDstgw,altPathWithoutAttacker)].append(duringLinkLost)
                conflictConfigs[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,hopsToSpoofed,isForwarding,hopsFromSpoofedToDest,spoofedBetweenAttacker,isDstBetweenSpoofedAndAttacker,spoofedBetweenAttackergw,isDstBetweenSpoofedAndAttackergw,isAttackerBetweenSpoofedAndDst,isAttackerBetweenSpoofedAndDstgw,isSrcBetweenSpoofedAndDst,isSrcBetweenSpoofedAndDstgw,altPathWithoutAttacker)].append((configName,duringLinkLost))
            #if it is in there and there is no conflict, then check if there has been a conflict, is yes, then add it.
            else:
                if len(uniques[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,hopsToSpoofed,isForwarding,hopsFromSpoofedToDest,spoofedBetweenAttacker,isDstBetweenSpoofedAndAttacker,spoofedBetweenAttackergw,isDstBetweenSpoofedAndAttackergw,isAttackerBetweenSpoofedAndDst,isAttackerBetweenSpoofedAndDstgw,isSrcBetweenSpoofedAndDst,isSrcBetweenSpoofedAndDstgw,altPathWithoutAttacker)]) > 1:                
                    uniques[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,hopsToSpoofed,isForwarding,hopsFromSpoofedToDest,spoofedBetweenAttacker,isDstBetweenSpoofedAndAttacker,spoofedBetweenAttackergw,isDstBetweenSpoofedAndAttackergw,isAttackerBetweenSpoofedAndDst,isAttackerBetweenSpoofedAndDstgw,isSrcBetweenSpoofedAndDst,isSrcBetweenSpoofedAndDstgw,altPathWithoutAttacker)].append(duringLinkLost)
                    conflictConfigs[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,hopsToSpoofed,isForwarding,hopsFromSpoofedToDest,spoofedBetweenAttacker,isDstBetweenSpoofedAndAttacker,spoofedBetweenAttackergw,isDstBetweenSpoofedAndAttackergw,isAttackerBetweenSpoofedAndDst,isAttackerBetweenSpoofedAndDstgw,isSrcBetweenSpoofedAndDst,isSrcBetweenSpoofedAndDstgw,altPathWithoutAttacker)].append((configName,duringLinkLost))
                        
#do the ones that are not the majority
configsToDo = {}

for item in conflictConfigs:
    if len(conflictConfigs[item]) > 1:
        #count number of falses and trues
        numFalses = 0
        numTrues = 0
        todo = "both"
        for subitem in conflictConfigs[item]:
            if subitem[1] == "true":
                numTrues +=1
            else:
                numFalses +=1
        if numTrues > numFalses:
            todo = "false"
        elif numTrues < numFalses:
            todo = "true"
        else: todo = "both"
        
        for subitem in conflictConfigs[item]:
            if subitem[1] == todo or todo == "both":
                configsToDo[subitem[0]] = (numTrues,numFalses)  
print "#!/bin/bash"

for item in configsToDo:
    print "rm ./"+item+" -rf"

for item in uniques:
    if len(uniques[item]) > 1:
        print item,uniques[item]
print len(configsToDo)
for item in configsToDo:
    print item,configsToDo[item]

#do the ones that are evenly split
#print "Found",numConflicts,"conflicts among ",len(configConflictCounts),"configs,",numRedo,"are above",minForRedo
