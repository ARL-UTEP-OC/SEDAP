'''
Created on Mar 22, 2016

@author: epadilla2
'''
from Converter import Converter
import sys
import networkx as nx
import xml.etree.ElementTree as ET
from lxml import etree
from netaddr import *
import logging

class PConverter(Converter):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def readHacl(self,filePath):
        self.haclFilePath = filePath
        file = open(filePath)
        return file.read()
    
    def readEvaluatedFlow(self,filePath):
        self.evaluatedFlowsFilePath = filePath
        file = open(filePath)
        return file.read()
    
    def convert(self): 
        #input files are: 
        #2. topology             (typically sampleInput_hacls.txt)
        #3. hijacking results  (typically sampleInput_model.xml)
        '''
        if len(sys.argv) != 3:
            print """
        usage: 
        python AGAggregator.py <input1> <input2>
        input files are: 
        1. topology             (typically sampleInput_hacls.txt)
        2. hijacking results  (typically sampleInput_model.xml)    
        """
            exit()
        '''
        
        hacls_file = open(self.haclFilePath, "r")
        model_file = open(self.evaluatedFlowsFilePath, "r")
        
        output = "/******File auto-generated from AGAggregator.py**********/\n"
        output += "/* Network Topology Definitions:*/\n"
        for line in hacls_file.readlines():
            output += line
        
        output+="\n"
        output += "/* Flow Definitions: */\n"
        #Process the flows in the flowDescriptionAttributes model file:
        root = ET.parse(model_file).getroot()
        
        numFlows = 1
        attributeValues = {}
        
        #attackVictimAttributes will hold values used to define the attackerGoal and services
        #ideally these will be manually entered, but I'll use this for automating several executions
        attackVictimAttributes = {}
        attackVictimAttributes["attackNode"] = []
        attackVictimAttributes["victim"] = []
        attackVictimAttributes["src"] = []
        attackVictimAttributes["dst"] = []
        attackVictimAttributes["typeName"] = []
        attackVictimAttributes["flowAccount"] = []
        
        for flowDescriptionAttribute in root.findall('FlowDescriptionAttributes'):
            for attribute in flowDescriptionAttribute.findall('Attribute'):
                attributeValues[attribute.find('Name').text] = str(attribute.find('Value').text)
            output += "/* Flow #"+str(numFlows)+" :*/\n"
            src = attributeValues["src"]
            dst = attributeValues["dst"]
            typeName = attributeValues["typeName"]
            routingProgram = attributeValues["routingProgram"]
            routingProtocol = attributeValues["routingProtocol"]
            duringLinkLost =  attributeValues["duringLinkLost"]
            
            #should always be present; ideally only one copy in an xml attribute, but its in a tag :(
            attackVictimAttributes["attackNode"].append(attributeValues["attackNode"])
            
            #append the flow
            output += "flowExists("+str(src)+","+str(dst)+", "+typeName+", "+"_port, flow"+str(numFlows)+"Account).\n"
            #the account
            output += "hasAccount(flow"+str(numFlows)+"Principal,"+dst+", flow"+str(numFlows)+"Account).\n"
            if duringLinkLost == 'True':
                routingProgramVul = routingProgram[:-1] +"Vul'"
                #the routing protocol used
                output += "networkServiceInfo("+str(src)+","+str(routingProgram)+", "+routingProtocol+", "+"_NA_port_layer3, "+"_NA_perm_layer3"+").\n"
                #if duringLinkLost is true, then we add the vulnerability associated with the routing protocol used
                output += "vulExists("+str(src)+","+str(routingProgramVul)+", "+str(routingProgram)+", remoteExploit, "+"nrlolsrHijack"+").\n"
        
                attackVictimAttributes["victim"].append(attributeValues["victim"])
                attackVictimAttributes["src"].append(attributeValues["src"])
                attackVictimAttributes["dst"].append(attributeValues["dst"])
                attackVictimAttributes["typeName"].append(attributeValues["typeName"])
                attackVictimAttributes["flowAccount"].append("flow"+str(numFlows)+"Account")
            output += "\n"
            numFlows += 1
        
        output += "/******Attacker Located:**********/\n"    
        if len(attackVictimAttributes["attackNode"]) > 0:
            #accessing the 0 position because they should all be the same (for now).
            output += "attackerLocated("+str(attackVictimAttributes["attackNode"][0])+").\n"
        else:
            output += "/* No attackNode was specified!!*/\n"
        output+="\n"
        
        output += "/******Semi-Auto definitions (please modify if needed):**********/\n"    
        #using the 0 position because we'll assume the first vulnerable is the chosen victim
        if len(attackVictimAttributes["dst"]) > 0:
            output += "attackGoal(execCode("+attackVictimAttributes["dst"][0]+", _)).\n"
        else:
            output += "/* No routing vulnerabilities were found!!*/\n"
        output+="\n"
        
        output += "/******Manual definitions should go here:**********/\n"
        #this should be removed before production use:
        output += "/** Temporary for testing (we're assuming there is a login service for each dst in each flow)**/\n"
        if len(attackVictimAttributes["dst"]) > 0 and len(attackVictimAttributes["typeName"]) > 0 and len(attackVictimAttributes["flowAccount"]) > 0:
            for i in range(0,len(attackVictimAttributes["dst"])):
                output += "networkServiceInfo("+attackVictimAttributes["dst"][i]+" , ftpd, "+attackVictimAttributes["typeName"][i]+" , _port, "+attackVictimAttributes["flowAccount"][i]+").\n"
        
        self.outputStr = output
        return self.outputStr
    