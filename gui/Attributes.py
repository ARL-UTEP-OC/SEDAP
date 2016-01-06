'''
Created on Dec 20, 2015

@author: Edgar
'''
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

class Attributes(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
    
    def readXML(self, filePath):
        print "reading xml"
        self.tree = ET.parse(filePath)
        root = self.tree.getroot()
        
        # declaring dictionary
        flowAttributes = dict()
        
        for attribute in root.findall('Attribute'):
            flowAttributes[attribute.find('Name').text] = str(attribute.find('Value').text)
        
        return flowAttributes
    
    def writeXML(self,filePath,flowAttributes):
        root = ET.Element('FlowDescriptionAttributes')
        #comment = ET.Comment('Generated for GUI')
        #document.append(comment)
        
        for key, value in flowAttributes.iteritems():
            attribute = ET.SubElement(root , 'Attribute')
            ET.SubElement(attribute, 'Name').text = key
            ET.SubElement(attribute, 'Value').text = value
            
        self.tree = ET.ElementTree(root)
        #root.write(filePath)
        prettyXml = self.prettify(root)
        text_file = open(filePath, "w")
        #text_file.write(self.prettify(self.tree ))
        text_file.write(self.prettify(root))
        print prettyXml
        
    def toString(self):
        root = self.tree.getroot()
        return self.prettify(root)
        #return self.prettify(self.tree)
    
    def prettify(self,root):
        rough_string = ET.tostring(root, 'utf-8',method="xml")
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml()