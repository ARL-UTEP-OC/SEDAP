'''
Created on Mar 22, 2016

@author: epadilla2
'''
import sys
from AttributeConverter import AttributeConverter
from RuleConverter import RuleConverter
from RouteConverter import RouteConverter
from ModelEvaluator import ModelEvaluator
from PConverter import PConverter

class Workflow(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
if __name__ == "__main__":
    
    
    if len(sys.argv) != 3:
        print "Error: Please enter the location of thw files"
        
    routesPath = sys.argv[1]
    wekaRules = sys.argv[2]
    
    routes = RouteConverter()
    routes.readRoutes(routesPath)
    routes.convert()
    routes.writeOutput("standardAttributes.xml")
    print "Converted CORE routes to standard format"
    print "Generated HACL topology"
        
    attr = AttributeConverter()
    attr.readXML("standardAttributes.xml")
    print "Loaded attribute flow"
        
    rules = RuleConverter()
    rules.readFromFile(wekaRules)
    rules.convert()
    rules.writeOutput("Model.py")
    print "Converted Weka rules to Python Model"
        
    model = ModelEvaluator()
    model.readFromFile("Model.py")
    model.evaluate(attr.attributes)
    model.writeModelEvaluationXML("EvaluatedFlow.xml",attr.attributes,model.evaluationResults)
    print "Evaluated Python Model"
    
    p = PConverter()
    p.readHacl("hacls.txt")
    p.readEvaluatedFlow("EvaluatedFlow.xml")
    p.convert()
    p.writeOutput("mulvalInput.P")
    print "Generated P file for Mulval given HACL and Model"
    
    
    
    
    