'''
Created on Mar 22, 2016

@author: epadilla2
'''
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

class Converter(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        pass
    
    def readFromFile(self,filePath):
        self.filePath = filePath
        file = open(filePath)
        return file.read()
    
    def writeXML(self,fileName,attributes):
        prettyXml = self.toXMLString(attributes)
        # print prettyXml
        text_file = open(fileName, "w")
        text_file.write(prettyXml)
        text_file.close()
        
    def prettify(self,root):
        rough_string = ET.tostring(root, 'utf-8',method="xml")
        reparsed = minidom.parseString(rough_string) # comment to stop prettyfy
        return reparsed.toprettyxml() # comment to stop prettyfy
        ##return rough_string # uncoment for ugly xml
        
    def writeOutput(self, fileName, text = None):
        if text is None:
            text = self.outputStr
        text_file = open(fileName, "w")
        text_file.write(text)
        text_file.close()