#!/usr/bin/python
'''
Created on Mar 22, 2016

@author: epadilla2
'''
import sys
from DataProcessors.AttributeConverter import AttributeConverter
from DataProcessors.ModelConverter.ModelConverter import ModelConverter
from DataProcessors.AttributesExtractor.AttributesExtractor import AttributesExtractor
from DataProcessors.ModelEvaluator.ModelEvaluator import ModelEvaluator
from DataProcessors.AGInputGenerator.AGInputGenerator import AGInputGenerator

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
1. route information (typically ./simpleScenario/input/sampleInputMilcom.xml)
2. weka rules (typically ./simpleScenario/input/OLSR_Spoofing.REPTree)	
3. output folder (typically ./simpleScenario/output/)
"""
       exit()
        
    routesPath = sys.argv[1]
    wekaRules = sys.argv[2]
    outputPath = sys.argv[3] +"/"
    
    
    routes = AttributesExtractor()
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
        
    rules = ModelConverter()
    rules.readFromFile(wekaRules)
    rules.convert()
    rules.writeOutput(outputPath+"Model.py")
    print "Converted Weka rules to Python Model"
        
    model = ModelEvaluator()
    model.readFromFile(outputPath+"Model.py")
    model.evaluate(attr.attributes)
    model.writeModelEvaluationXML(outputPath+"EvaluatedFlow.xml",attr.attributes,model.evaluationResults)
    print "Evaluated Python Model"
    
    p = AGInputGenerator()
    p.readHacl(outputPath+"hacl.txt")
    p.readEvaluatedFlow(outputPath+"EvaluatedFlow.xml")
    p.convert()
    p.writeOutput(outputPath+"mulvalInput.P")
    print "Generated P file for Mulval given HACL and Model"
    
	
