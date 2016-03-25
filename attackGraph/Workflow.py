#!/usr/bin/python
'''
Created on Mar 22, 2016

@author: epadilla2
'''
import sys
from gui.AttributeConverter import AttributeConverter
from gui.RuleConverter import RuleConverter
from gui.RouteConverter import RouteConverter
from gui.ModelEvaluator import ModelEvaluator
from gui.PConverter import PConverter

class Workflow(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
if __name__ == "__main__":
    
    if len(sys.argv) != 4:
       print """
usage: 
python Workflow.py <input1> <input2> <input3>
input files are: 
1. route information (typically ./AttributesGenerator/sampleInput.xml)
2. weka rules (typically ./ModelConverter/OLSR_Forwarding.REPTree.rules)	
3. output folder (typically ./outputFiles)
"""
       exit()
        
    routesPath = sys.argv[1]
    wekaRules = sys.argv[2]
    outputPath = sys.argv[3] +"/"
    
    
    routes = RouteConverter()
    routes.readRoutes(routesPath)
    routes.convert()
    routes.getAttributes()
    routes.writeOutput(outputPath+"standardAttributes.xml")
    print "Converted node routes to attributes"
    routes.getHacl()
    routes.writeOutput(outputPath+"hacl.txt")
    print "Generated HACL topology"
        
    attr = AttributeConverter()
    attr.readXML(outputPath+"standardAttributes.xml")
    print "Loaded attribute flow"
        
    rules = RuleConverter()
    rules.readFromFile(wekaRules)
    rules.convert()
    rules.writeOutput(outputPath+"Model.py")
    print "Converted Weka rules to Python Model"
        
    model = ModelEvaluator()
    model.readFromFile(outputPath+"Model.py")
    model.evaluate(attr.attributes)
    model.writeModelEvaluationXML(outputPath+"EvaluatedFlow.xml",attr.attributes,model.evaluationResults)
    print "Evaluated Python Model"
    
    p = PConverter()
    p.readHacl(outputPath+"hacl.txt")
    p.readEvaluatedFlow(outputPath+"EvaluatedFlow.xml")
    p.convert()
    p.writeOutput(outputPath+"mulvalInput.P")
    print "Generated P file for Mulval given HACL and Model"
    
	
