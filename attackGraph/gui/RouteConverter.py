'''
@author: Dr. Jaime Acosta
'''
#!/usr/bin/python
import sys
import networkx as nx
import xml.etree.ElementTree as ET
from lxml import etree
from netaddr import *
import logging
from Converter import Converter

class RouteConverter(Converter):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
         #globals
        self.gateways = {} #(src, dest) -> (gateway, metric)
        self.directLinks = {} #(src, dest) -> ('0.0.0.0', metric)
        self.G = nx.Graph()
        self.nodes = {} 
        
        self.attackName = ""
        self.victim = None
        self.attackNode = None
        self.flows = [] #(src, dest, type)
        
        #Create the root element for the output file:
        self.attributesXML = etree.Element("Attributes")
        
        #parameters for output
        self.flowDescriptionAttributes = {}
        self.flowDescriptionAttributes["src"]=''
        self.flowDescriptionAttributes["dst"]=''
        self.flowDescriptionAttributes["attackNode"]=''
        self.flowDescriptionAttributes["victim"]=''
        self.flowDescriptionAttributes["routingProgram"]=''
        self.flowDescriptionAttributes["routingProtocol"]=''
        self.flowDescriptionAttributes["victim"]=''
        self.flowDescriptionAttributes["fromHop"]=''
        self.flowDescriptionAttributes["toHop"]=''
        self.flowDescriptionAttributes["typeName"]=''
        self.flowDescriptionAttributes["distance"]=''
        self.flowDescriptionAttributes["passthrough"]=''
        self.flowDescriptionAttributes["srcSpoofed"]=''
        self.flowDescriptionAttributes["destSpoofed"]=''
        self.flowDescriptionAttributes["hopsToSpoofed"]=''
        self.flowDescriptionAttributes["hopsFromSpoofedToDest"]=''
        self.flowDescriptionAttributes["spoofedBetweenAttacker"]=''
        self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttacker"]=''
        self.flowDescriptionAttributes["spoofedBetweenAttackergw"]=''
        self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]=''
        self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDst"]=''
        self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]=''
        self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDst"]=''
        self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]=''
        self.flowDescriptionAttributes["altPathWithoutAttacker"]=''


    def extractLinksfromRoutes(self, nodeIP, routes):
    
        #initialize the elements string
        elements = ""
        #remove extra spaces:
        for line in routes.split('\n'):
            line = ' '.join(line.split())
            elements = line.split(" ")
            #ignore if the destination subnet is 0.0.0.0 or multicast 224...
            if elements[0] == '0.0.0.0' or elements [0].startswith('224.'):
                continue
            #otherwise, if 2nd column is 0.0.0.0, then this is a direct link
            dst = elements[0] + "/" + elements[2]
            if elements[1] == '0.0.0.0':
                self.directLinks[(nodeIP,IPNetwork(dst))] = (elements[1], elements[4])
                #also add direct links to our networkx graph for later processing
                self.G.add_edge(nodeIP,IPNetwork(dst))
            #otherwise, this we extract the gateway
            else:
                self.gateways[(nodeIP,IPNetwork(dst))] = (elements[1], elements[4])
    
    def getPathThroughGW(self,src, dst):
        path = []
        curr = ()
        if (src, dst) in self.directLinks:
            path.append(dst)
            return path
        if (src, dst) not in self.gateways:
            return None
        #get next hop
        curr = self.gateways[(src,dst)]
        while curr != None:
            #need to do the following lookup to re-obtain the netmask for the current IP address
            #convert string to IPAddress
            curr = IPAddress(curr[0])
            #now get entry with netmask
            if curr not in self.nodes:
                #somethings wrong...
                print curr,"not found in nodes list!"
                curr = None
                return None
            curr = self.nodes[curr]
            path.append(curr)
            if (curr,dst) in self.directLinks:
                curr = self.directLinks[(curr,dst)]
                #found a direct link so we're done
                path.append(dst)
                curr = None
            elif (curr, dst) in self.gateways:
                curr = self.gateways[(curr,dst)]
            else:
                print curr,"no path found!"
                curr = None
                return None            
        return path
    
    def getSubPath(self,param1, param2):
        answer = []
        #check if param1 is a subpath of param2
        if len(param1) > len(param2):
            return []
        for i in range(0,len(param1)):
            if param1[i] == param2[i]:
                answer.append(param1[i])
            else:
                return answer
        return answer
        
    
    def generateParametersFromTrafficProfile(self):
        
        for flow in self.flows:
            
            #flowDescriptionAttributes["attackNode"]
            self.flowDescriptionAttributes["attackNode"] = "'"+str(self.attackNode)+"'"
            logging.debug("attackNode %s",self.flowDescriptionAttributes["attackNode"])
    
            #flowDescriptionAttributes["victim"]
            self.flowDescriptionAttributes["victim"] = "'"+str(self.victim)+"'"
            logging.debug("victim %s",self.flowDescriptionAttributes["victim"])
            
            src = flow[0]
            dst = flow[1]
                        
            #flowDescriptionAttributes["src"]
            self.flowDescriptionAttributes["src"] = "'"+str(src)+"'"
            logging.debug("src %s",self.flowDescriptionAttributes["src"])
            
            #flowDescriptionAttributes["dst"]
            self.flowDescriptionAttributes["dst"] = "'"+str(dst)+"'"
            logging.debug("dst %s",self.flowDescriptionAttributes["dst"])
    
            #flowDescriptionAttributes["routingProgram"]
            self.flowDescriptionAttributes["routingProgram"] = "'"+str(self.routingProgram)+"'"
            logging.debug("routingProgram %s",self.flowDescriptionAttributes["routingProgram"])
            
            #flowDescriptionAttributes["routingProtocol"]
            self.flowDescriptionAttributes["routingProtocol"] = "'"+str(self.routingProtocol)+"'"
            logging.debug("routingProtocol %s",self.flowDescriptionAttributes["routingProtocol"])
            
            #flowDescriptionAttributes["fromHop"]
            logging.debug( "looking for: %s",(self.attackNode,src))
            if ((self.attackNode,src)) in self.directLinks:
                self.flowDescriptionAttributes["fromHop"] = self.directLinks[(self.attackNode,src)][1]
            elif ((self.attackNode,src)) in self.gateways:
                self.flowDescriptionAttributes["fromHop"] = self.gateways[(self.attackNode,src)][1]
            else:
                print self.flowDescriptionAttributes["fromHop"],"not found"
                exit
            logging.debug("fromHop %s",self.flowDescriptionAttributes["fromHop"])
    
            #flowDescriptionAttributes["toHop"]
            logging.debug("looking for: %s",(self.attackNode,dst))
            if ((self.attackNode,dst)) in self.directLinks:
                self.flowDescriptionAttributes["toHop"] = self.directLinks[(self.attackNode,dst)][1]
            elif ((self.attackNode,dst)) in self.gateways:
                self.flowDescriptionAttributes["toHop"] = self.gateways[(self.attackNode,dst)][1]
            else:
                print self.flowDescriptionAttributes["toHop"],"not found"
                exit
            logging.debug("toHop %s",self.flowDescriptionAttributes["toHop"])
            
            #type
            typeName = flow[2]
            if typeName.startswith("'") == False:
                typeName = "'"+flow[2]
            if typeName.endswith("'") == False:
                typeName = typeName+"'"
            self.flowDescriptionAttributes["typeName"] = typeName
            logging.debug("type %s",self.flowDescriptionAttributes["typeName"])
            
            #flowDescriptionAttributes["distance"]
            logging.debug("looking for:  %s",(src,dst))
            if ((src,dst)) in self.directLinks:
                self.flowDescriptionAttributes["distance"] = self.directLinks[(flow[0],dst)][1]
            elif ((src,dst)) in self.gateways:
                self.flowDescriptionAttributes["distance"] = self.gateways[(src,dst)][1]
            else:
                print self.flowDescriptionAttributes["distance"],"not found"
                exit
            logging.debug("distance %s",self.flowDescriptionAttributes["distance"])
            ###path function test
            logging.debug("looking for path:  %s",(src,dst))
            logging.debug("\nPath\n %s",self.getPathThroughGW(src, dst))
            ###
            
            logging.debug("\npassthrough check:  %s  in %s",self.attackNode, (src,dst))
            if self.attackNode in self.getPathThroughGW(src,dst):
                self.flowDescriptionAttributes["passthrough"]="True"
            else:
                self.flowDescriptionAttributes["passthrough"]="False"
    ########The following parameters are only valid if attack is spoofing#####
            logging.debug("\nsrc spoofed:  %s %s",src, self.victim)
            if src == self.victim:
                self.flowDescriptionAttributes["srcSpoofed"]="True"
            else:
                self.flowDescriptionAttributes["srcSpoofed"]="False"
            logging.debug("srcSpoofed %s",self.flowDescriptionAttributes["srcSpoofed"])
    
            logging.debug("\ndst spoofed:  %s %s",dst, self.victim)
            if dst == self.victim:
                self.flowDescriptionAttributes["destSpoofed"]="True"
            else:
                self.flowDescriptionAttributes["destSpoofed"]="False"
            logging.debug("destSpoofed %s",self.flowDescriptionAttributes["destSpoofed"])
    
            logging.debug("checking hopsToSpoofed from: %s to %s",self.attackNode,self.victim)
            if (self.attackNode,self.victim) in self.directLinks:
                self.flowDescriptionAttributes["hopsToSpoofed"]=self.directLinks[(self.attackNode,self.victim)][1]
            elif (self.attackNode,self.victim) in self.gateways:
                self.flowDescriptionAttributes["hopsToSpoofed"]=self.gateways[(self.attackNode,self.victim)][1]
            else: 
                self.flowDescriptionAttributes["hopsToSpoofed"]='-1'
            logging.debug("hopsToSpoofed %s",self.flowDescriptionAttributes["hopsToSpoofed"])
                
            logging.debug("checking hopsFromSpoofedToDest from: %s to %s",self.victim,dst)
            if (self.victim,dst) in self.directLinks:
                self.flowDescriptionAttributes["hopsFromSpoofedToDest"]=self.directLinks[(self.victim,dst)][1]
            elif (self.victim,dst) in self.gateways:
                self.flowDescriptionAttributes["hopsFromSpoofedToDest"]=self.gateways[(self.victim,dst)][1]
            else: 
                self.flowDescriptionAttributes["hopsFromSpoofedToDest"]='-1'
            logging.debug("hopsFromSpoofedToDest %s",self.flowDescriptionAttributes["hopsFromSpoofedToDest"]    )
            
            logging.debug("checking spoofedBetweenAttacker. Is: %s between (or equal to either) %s to %s",self.victim,src,self.attackNode)
            if self.victim == src:
                self.flowDescriptionAttributes["spoofedBetweenAttacker"]="True"
            elif self.victim in self.getPathThroughGW(src,self.attackNode):
                self.flowDescriptionAttributes["spoofedBetweenAttacker"]="True"
            else:
                self.flowDescriptionAttributes["spoofedBetweenAttacker"]="False"
            logging.debug("spoofedBetweenAttacker %s",self.flowDescriptionAttributes["spoofedBetweenAttacker"])
            
            logging.debug("checking isDstBetweenSpoofedAndAttacker. Is: %s between (or equal to either) %s to %s",dst,self.victim,self.attackNode)
            if dst == self.victim:
                self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttacker"]="True"
            elif dst in self.getPathThroughGW(self.victim,self.attackNode):
                self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttacker"]="True"
            else:
                self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttacker"]="False"
            logging.debug("isDstBetweenSpoofedAndAttacker %s",self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttacker"])
            
    #######
            #algorithm used to check: if path(src,dst) startswith(path(src,att)-1) true; else false
            logging.debug("checking spoofedBetweenAttackergw. Is %s between or is a gateway (or equal to either) %s to %s:",self.victim,src,self.attackNode)
            subPath = []
            if self.victim == src:
                self.flowDescriptionAttributes["spoofedBetweenAttackergw"]="True"
            else:
                #real path
                pathA = self.getPathThroughGW(src,self.attackNode)
                #path to "between" node
                pathB = self.getPathThroughGW(src,self.victim)
                #now check if pathA starts with pathB-1
                if len(pathB) == 0 and len(pathB) > len(pathA):
                    self.flowDescriptionAttributes["spoofedBetweenAttackergw"]="False"
                else:
                    pathB = pathB[:len(pathB)-1]
                    #check if param1 is a subpath of param2
                    subPath = self.getSubPath(pathB, pathA)
                    logging.debug("subPath of: %s %s %s \nSUBPATH: %s",src,self.victim,self.attackNode,subPath)
                    self.flowDescriptionAttributes["spoofedBetweenAttackergw"]="False"
            if len(subPath) == 0:
                self.flowDescriptionAttributes["spoofedBetweenAttackergw"]="False"
            else:
                self.flowDescriptionAttributes["spoofedBetweenAttackergw"]="True"
            logging.debug("spoofedBetweenAttackergw %s",self.flowDescriptionAttributes["spoofedBetweenAttackergw"])
    
    #######
            logging.debug("checking isDstBetweenSpoofedAndAttackergw Is: %s between or is a gateway (or equal to either) %s to %s",self.victim,dst,self.attackNode)
            subPath = []
            if self.victim == dst:
                self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]="True"
            else:
                #real path
                pathA = self.getPathThroughGW(dst,self.attackNode)
                #path to "between" node
                pathB = self.getPathThroughGW(dst,self.victim)
                #now check if pathA starts with pathB-1
                if len(pathB) == 0 and len(pathB) > len(pathA):
                    self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]="False"
                else:
                    pathB = pathB[:len(pathB)-1]
                    #check if param1 is a subpath of param2
                    subPath = self.getSubPath(pathB, pathA)
                    logging.debug("subPath of: %s %s %s \nSUBPATH: %s",dst,self.victim,self.attackNode,subPath)
                    self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]="False"
            if len(subPath) == 0:
                self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]="False"
            else:
                self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"]="True"
            logging.debug("isDstBetweenSpoofedAndAttackergw %s",self.flowDescriptionAttributes["isDstBetweenSpoofedAndAttackergw"])
    
    #######
            logging.debug("checking isAttackerBetweenSpoofedAndDst. Is: %s between (or equal to either) %s to %s",self.attackNode,self.victim,dst)
            if self.attackNode == self.victim:
                self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDst"]="True"
            elif self.attackNode in self.getPathThroughGW(self.victim,dst):
                self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDst"]="True"
            else:
                self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDst"]="False"
            logging.debug("isAttackerBetweenSpoofedAndDst %s",self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDst"])
    
    #######
    
            logging.debug("checking isAttackerBetweenSpoofedAndDstgw Is: %s between or is a gateway (or equal to either) %s to %s",self.attackNode,self.victim,dst)
            subPath = []
            if self.attackNode == self.victim:
                self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]="True"
            else:
                #real path
                pathA = self.getPathThroughGW(self.victim,dst)
                #path to "between" node
                pathB = self.getPathThroughGW(self.victim,self.attackNode)
                #now check if pathA starts with pathB-1
                if len(pathB) == 0 and len(pathB) > len(pathA):
                    self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]="False"
                else:
                    pathB = pathB[:len(pathB)-1]
                    #check if param1 is a subpath of param2
                    subPath = self.getSubPath(pathB, pathA)
                    logging.debug("subPath of: %s %s %s \nSUBPATH: %s",self.victim,self.attackNode,dst,subPath)
                    self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]="False"
            if len(subPath) == 0:
                self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]="False"
            else:
                self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"]="True"
            logging.debug("isAttackerBetweenSpoofedAndDstgw %s",self.flowDescriptionAttributes["isAttackerBetweenSpoofedAndDstgw"])
        
            
    #######
    #21. isSrcBetweenSpoofedAndDst    -- src between vic and dst
    #######
            logging.debug("checking isSrcBetweenSpoofedAndDst. Is: %s between (or equal to either) %s to %s",src,self.victim,dst)
            if src == self.victim:
                self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDst"]="True"
            elif src in self.getPathThroughGW(self.victim,dst):
                self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDst"]="True"
            else:
                self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDst"]="False"
            logging.debug("isSrcBetweenSpoofedAndDst %s",self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDst"])
    
    
    #######    
    #22. self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]    -- src a gw of any node between vic and dst
    
            logging.debug("checking isSrcBetweenSpoofedAndDstgw Is: %s between or is a gateway (or equal to either) %s to %s",src,self.victim,dst)
            subPath = []
            if src == self.victim:
                self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]="True"
            else:
                #real path
                pathA = self.getPathThroughGW(self.victim,dst)
                #path to "between" node
                pathB = self.getPathThroughGW(self.victim,src)
                #now check if pathA starts with pathB-1
                if len(pathB) == 0 and len(pathB) > len(pathA):
                    self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]="False"
                else:
                    pathB = pathB[:len(pathB)-1]
                    #check if param1 is a subpath of param2
                    subPath = self.getSubPath(pathB, pathA)
                    logging.debug("subPath of: %s %s %s \nSUBPATH: %s",self.victim,src,dst,subPath)
                    self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]="False"
            if len(subPath) == 0:
                self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]="False"
            else:
                self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]="True"
            logging.debug("isSrcBetweenSpoofedAndDstgw %s",self.flowDescriptionAttributes["isSrcBetweenSpoofedAndDstgw"]    )
    
    #######    
    #23. flowDescriptionAttributes["altPathWithoutAttacker"]
    
    #clone the graph, remove the attacker and then check if a path exists from src to dst
            logging.debug("checking altPathWithoutAttacker: attackNode %s src: %s dst: %s",self.attackNode,src,dst)
            if not nx.has_path(self.G,src,dst):
                self.flowDescriptionAttributes["altPathWithoutAttacker"]="False"
            else:
                tmpGraph = self.G.copy()
                tmpGraph.remove_node(self.attackNode)
                if not nx.has_path(tmpGraph,src,dst):
                    self.flowDescriptionAttributes["altPathWithoutAttacker"]="False"
                else:
                    self.flowDescriptionAttributes["altPathWithoutAttacker"]="True"
            logging.debug("altPathWithoutAttacker %s",self.flowDescriptionAttributes["altPathWithoutAttacker"])
            logging.debug("\n\n")
            
            #######now generate XML tags:
            #print "Here!!!"
            flowDescriptionAttributesXML = etree.SubElement(self.attributesXML, "FlowDescriptionAttributes")
            
            for attribute in self.flowDescriptionAttributes:
                attributeXML = etree.SubElement(flowDescriptionAttributesXML, "Attribute")
                nameXML = etree.SubElement(attributeXML, "Name")
                nameXML.text = attribute
                valueXML = etree.SubElement(attributeXML, "Value")
                valueXML.text = self.flowDescriptionAttributes[attribute]
    
    
    #first read the input configuration xml file
    def readConfig(self,filename):     
        
        tree = ET.parse(filename)
        root = tree.getroot()
        scenarioConfig = root.find('scenario-config')
        self.attackName = scenarioConfig.find('attack-name').text.rstrip().lstrip()
        
        if self.attackName == "spoofingAttack":
            self.victim = IPNetwork(scenarioConfig.find('victim-node').text.rstrip().lstrip())
        else:
            print "Only works with spoofing attack for now!"
            exit()
        self.attackNode = IPNetwork(scenarioConfig.find('attack-node').text.rstrip().lstrip())
        
        self.routingProgram = scenarioConfig.find('routing-mechanism').find('program').text.rstrip().lstrip()
        self.routingProtocol = scenarioConfig.find('routing-mechanism').find('protocol').text.rstrip().lstrip()
        
        trafficProfile = scenarioConfig.find('traffic-profile')
        #extract the traffic flows
        for flow in trafficProfile.findall('flow'):
            self.flows.append((IPNetwork(flow.find('src').text.rstrip().lstrip()),IPNetwork(flow.find('dst').text.rstrip().lstrip()),flow.find('type').text.rstrip().lstrip()))
    
        #extract node information
        for node in scenarioConfig.findall('node'):
            name = node.find('name')
            nodeRoutes = node.find('routes').text.rstrip().lstrip()
            nodeIP = IPNetwork(node.find('ip-addresses').text.rstrip().lstrip())
            #want to keep track of IP addresses and their subnets for path lookup
            self.nodes[nodeIP.ip] = nodeIP.cidr
            #Extract links and metrics and store results in gateways{}
            self.extractLinksfromRoutes(nodeIP, nodeRoutes)
            self.nodes[name.text.rstrip().lstrip()] = 'test'
    
    def readRoutes(self, filePath):
        self.filePath = filePath
        file = open(filePath)
        return file.read()
    
    def convert(self):
        #Will eventually convert print to logging
        #logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        #filename = sys.argv[1]
        self.readConfig(self.filePath)
        logging.debug("Nodes\n%s", self.nodes)
        logging.debug("\nGateways\n%s",self.gateways)
        logging.debug("\nDirect Links\n%s",self.directLinks)
        logging.debug("\nG\n%s",self.G.edges())
        
        self.generateParametersFromTrafficProfile()
        
        hacls = open("hacls.txt", "w")
        hacls.write("/* edges in graph represent connections among nodes as well as gateways */\n")
        for edge in self.G.edges():
            hacls.write("hacl('"+str(edge[0])+"', '"+str(edge[1])+"',_proto,_port).\n")
            
        for edge in self.G:
            hacls.write("gateway('"+str(edge)+"').\n")
        self.outputStr = etree.tostring(self.attributesXML,pretty_print='true')
        return self.outputStr
