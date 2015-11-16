#!/usr/bin/python
import time
import thread
import sys
import commands
import ast

inputFileName = sys.argv[1]
protocol = sys.argv[2]
scenFile = sys.argv[3]
minForRedo = sys.argv[4]

arffFile = open(inputFileName)

conflictConfigs = {}

lines = arffFile.readlines()[27:]

uniques = {}
lineNum=27
for line in lines:
    lineNum+=1
    #print "processing line: ",lineNum,line
    #if lineNum > 49:
#        break
    if not line.strip():
        continue
    params = line.split(",")

    #need from,to,type,dist,passthrough,srcIsSpoofed,destIsSpoofed,duringLinkLost,afterLinkLost,attackName
    #2,3,4,5,6,19,20,21,22,23
    #print "len",len(params),"line",line
    attackNodeNum = params[0]
    fromHop = params[2]
    toHop = params[3]
    type = params[4]
    dist = params[5]
    passThrough = params[6]
    srcIsSpoofed = params[19]
    destIsSpoofed = params[20]
    duringLinkLost = params[21]
    afterLinkLost = params[22]
    attackName = params[23]
    
    if "spoof" in attackName:
             attackName = "spoofingAttack"+attackName.split(".")[3].strip()+"_sh" 
    else:
        attackName = "forwardingAttack_sh"
    configName = attackNodeNum+"_60_60_"+attackName+"_jaime_scen_"+protocol+"_"+scenFile+"_txt"
    isForwarding = "no"
    if "forwarding" in attackName:
        isForwarding = "yes"
    if(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,isForwarding) not in uniques:
        uniques[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,isForwarding)] = [(duringLinkLost,afterLinkLost)]
        
        conflictConfigs[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,isForwarding)] = [configName]
        #print "uniques size",len(uniques),"conflicts size",len(conflictConfigs) 
        #now check if it's the same value:
    else:
        if (duringLinkLost,afterLinkLost) not in uniques[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,isForwarding)]:
#           print "uniques",uniques
#           print "appending line:",lineNum,"vals:", fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,duringLinkLost,afterLinkLost
            uniques[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,isForwarding)].append((duringLinkLost,afterLinkLost))
            if configName not in conflictConfigs[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,isForwarding)]:
                conflictConfigs[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,isForwarding)].append(configName)
        #if it is in there and there is no conflict, then check if there has been a conflict, is yes, then add it.
        else:
            if len(uniques[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,isForwarding)]) > 1:                
                uniques[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,isForwarding)].append((duringLinkLost,afterLinkLost))
                if configName not in conflictConfigs[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,isForwarding)]:
                    conflictConfigs[(fromHop,toHop,type,dist,passThrough,srcIsSpoofed,destIsSpoofed,isForwarding)].append(configName)
                    
#print "Found",numConflicts,"conflicts",
#print item,conflicts[item]
#print "or",numConflicts
#print "Recommend running the following and re-running experiment:"
configReRuns = 0
configConflictCounts = {}

for item in conflictConfigs:
    if len(conflictConfigs[item]) > 1:
        configReRuns+=len(conflictConfigs[item])
        for subitem in conflictConfigs[item]:
            if subitem not in configConflictCounts:
                configConflictCounts[subitem] = 1
            else:
                configConflictCounts[subitem]=configConflictCounts[subitem]+1

#now get the files with the most conflicts > 2
numRedo =0
print "#!/bin/bash"
for item in configConflictCounts:
    if configConflictCounts[item] > int(minForRedo):
        numRedo+=1
        print "rm ./"+item+" -rf"
        #print item,configConflictCounts[item]
    
numConflicts =0
for item in uniques:
     if len(uniques[item]) > 1:
         numConflicts+=len(uniques[item])-1
         print item,uniques[item]
             
#do the ones that are not the majority
#do the ones that are evenly split
print "Found",numConflicts,"conflicts among ",len(configConflictCounts),"configs,",numRedo,"are above",minForRedo