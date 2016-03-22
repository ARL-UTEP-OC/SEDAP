'''
Created on Mar 22, 2016

@author: epadilla2
'''
import sys
from AttributeConverter import AttributeConverter
from RuleConverter import RuleConverter
from RouteConverter import RouteConverter
from ModelEvaluator import ModelEvaluator

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
    
    attr = AttributeConverter()
    attr.readXML("standardAttributes.xml")
        
    rules = RuleConverter()
    rules.readFromFile(wekaRules)
    rules.convert()
    rules.writeOutput("Model.py")
        
    model = ModelEvaluator()
    model.readFromFile("Model.py")
    print model.evaluate(attr.attributes)
    