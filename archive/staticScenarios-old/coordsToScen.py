#!/usr/bin/python
import time
import thread
import sys

coordsFile = sys.argv[1]
scenName = sys.argv[2]

coords = open(coordsFile)
scen = open(scenName, 'w')
lineNum = 0
scen.write("# nodes: 10, max time: 180.00, max x: 600.00, max y: 600.00\r\n")

for line in coords.readlines():
    lineNum+=1
    pos = line.rstrip("\r\n").split(" ")
        
    scen.write("$node_("+str(lineNum)+") set X_ " + pos[0] + "\r\n")
    scen.write("$node_("+str(lineNum)+") set Y_ " + pos[1] + "\r\n")
    scen.write("$node_("+str(lineNum)+") set Z_ 0.0" + "\r\n")
scen.write("$ns_ at 180.00 \"$node_("+str(lineNum)+") setdest "+ pos[0] + " " + pos[1] + " 0.0\"\r\n")
