#!/usr/bin/python

import sys
import string
import os
import random

scenario = "jaime.scen"
startTime = 60
numNodes = 10
iterationsPerProtocol = 1

coordFiles = ["10x10.txt"]
protocols = ["OLSR" "OSPFv3MDR"]
attacks = ["spoofingAttack.sh","forwardingAttack.sh","downAttack.sh"]

for coordFile in coordFiles:
    print coordFile
    for protocol in protocols:
        print protocol
        for i in range(iterationsPerProtocol):
            nodeNum = random.randint(1,numNodes)
            attackRnd = random.randint(0,len(attacks)-1)
            attack = attacks[random.randint(0,len(attacks)-1)]
            if "spoofingAttack.sh" in attack:
                attackRnd = random.randint(1,numNodes)
                while nodeNum == attackRnd:
                    attackRnd = random.randint(1,numNodes)
                attack += str(attackRnd) 
            imnName=str(nodeNum)+"_"+str(startTime)+"_60_"+attack+"_"+scenario+"_"+protocol+"_"+coordFile
            imnName = string.replace(imnName, ".", "_")
            print imnName
            if not os.path.isdir("/root/"+imnName):
                os.system("rm /tmp/check.txt")
                os.system("rm /tmp/wireshark*")
                os.system("rm /tmp/maxn*")
                execStr = "./imnGenerator.py " + str(startTime) + " 60 " + str(numNodes) + " " + str(nodeNum) + " " + attack + " " + scenario + " " + protocol + " " +  coordFile + " > core/.core/configs/"+imnName+".imn"
                print execStr
                os.system(execStr)
                execStr = "core-gui -s core/.core/configs/"+imnName+".imn"
                print execStr
                os.system(execStr)
