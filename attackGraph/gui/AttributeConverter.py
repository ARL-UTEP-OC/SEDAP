'''
Created on Dec 20, 2015

@author: Edgar
'''
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from Converter import Converter

class AttributeConverter(Converter):

    def __init__(self):
        '''
        Constructor
        '''
    
    def readXML(self, filePath):
        print "reading xml"
        self.tree = ET.parse(filePath)
        root = self.tree.getroot()
        
        #declaring list 
        self.attributes = list()
        # declaring dictionary
        for flowAttribute in root.findall('FlowDescriptionAttributes'):
            flowAttributes = dict()
            for attribute in flowAttribute.findall('Attribute'):
                flowAttributes[attribute.find('Name').text] = str(attribute.find('Value').text)
            self.attributes.append(flowAttributes)
        
        return self.attributes
    
    def readARFF(self, filePath):
        print "reading arff"
        #declaring list 
        attributes = list()
        file = open(filePath, 'r')
        data = False
        for line in file:
            
            if "@data"  in line: 
                data = True
                continue
            if data == True:
                # declaring dictionary
                flowAttributes = dict()
                attr = line.split(',')
                if len(attr) <= 1:
                    continue
                flowAttributes["fromHop"]=attr[3]
                flowAttributes["toHop"]=attr[4]
                flowAttributes["type"]=attr[5]
                flowAttributes["distance"]=attr[6]
                flowAttributes["passthrough"]=attr[7]
                flowAttributes["beforeDelay"]=attr[8]
                flowAttributes["beforeMissed"]=attr[9]
                flowAttributes["beforeOOO"]=attr[10]
                flowAttributes["beforeNumPackets"]=attr[11]
                flowAttributes["srcSpoofed"]=attr[20]
                flowAttributes["destSpoofed"]=attr[21]
                flowAttributes["hopsToSpoofed"]=attr[22]
                flowAttributes["duringLinkLost"]=attr[23]
                flowAttributes["hopsFromSpoofedToDest"]=attr[26]
                flowAttributes["spoofedBetweenAttacker"]=attr[27]
                flowAttributes["isDstBetweenSpoofedAndAttacker"]=attr[28]
                flowAttributes["spoofedBetweenAttackergw"]=attr[29]
                flowAttributes["isDstBetweenSpoofedAndAttackergw"]=attr[30]
                flowAttributes["isAttackerBetweenSpoofedAndDst"]=attr[31]
                flowAttributes["isAttackerBetweenSpoofedAndDstgw"]=attr[32]
                flowAttributes["isSrcBetweenSpoofedAndDst"]=attr[33]
                flowAttributes["isSrcBetweenSpoofedAndDstgw"]=attr[34]
                flowAttributes["altPathWithoutAttacker"]=attr[35]
                attributes.append(flowAttributes)
        file.close()
                
        return attributes
              
    def toXMLString(self, attributes):
        root = ET.Element('Attributes')
        #comment = ET.Comment('Generated for GUI')
        #document.append(comment)
        for flowAttributes in attributes:
            flowAttribute = ET.SubElement(root , 'FlowDescriptionAttributes')
            for key, value in flowAttributes.iteritems():
                attribute = ET.SubElement(flowAttribute , 'Attribute')
                ET.SubElement(attribute, 'Name').text = key
                ET.SubElement(attribute, 'Value').text = value
            
        self.tree = ET.ElementTree(root)
        return self.prettify(root)