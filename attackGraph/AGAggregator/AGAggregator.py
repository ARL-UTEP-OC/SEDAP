#!/usr/bin/python
import sys
import networkx as nx
import xml.etree.ElementTree as ET
from lxml import etree
from netaddr import *
import logging

instance = ""

#globals

#input files are: 
#1. mulVAL input files (typically sampleInput_IPs.P)
#2. topology  		   (typically sampleInput_hacls.txt)
#3. hijacking results  (typically sampleInput_model.xml)

if len(sys.argv != 3):
	print """
usage: 
python AGAggregator.py <input1> <input2> <input3>
input files are: 
1. mulVAL input files (typically sampleInput_IPs.P)
2. topology  		   (typically sampleInput_hacls.txt)
3. hijacking results  (typically sampleInput_model.xml)	
"""
	exit()

mulVAL_file = open("sampleInput_IPs.P", "r")
hacls_file = open("sampleInput_hacls.txt", "r")
model_file = open("sampleInput_model.xml", "r")

#first open the model file and identify any "duringLinkLost=true" attributes

