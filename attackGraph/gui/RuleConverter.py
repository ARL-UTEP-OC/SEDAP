'''
Created on Mar 18, 2016

@author: epadilla2
'''
from Converter import Converter

class RuleConverter(Converter):
    '''
    classdocs
    '''
    
    def __init__(self):
        pass

    def convert(self):
        
        convRules =''
        rules = open(self.filePath)
    
        for line in rules:
            ans = ''
            
            numTabs = len(line.split('|'))
            line = line.replace('|','').replace("true","True").replace("false","False").lstrip()
            #need to change this so that it can extract other logical operators
            elements = line.split(' ')
            logicalOperator = elements[1]
            if logicalOperator == '=':
                logicalOperator = '=='
            varName = elements[0].strip()
            cmpVal = elements[2].strip()
            isNumber = cmpVal.replace('.','').replace('-','').isdigit()
            
            if isNumber == False:
                cmpVal = "'" + cmpVal + "'"
            if len(elements) > 3:
                ans = elements[4]
        
            indent = ''
            for i in range(0,numTabs+1):
                indent = indent + ' '
            if isNumber == True:
                convRules =convRules+indent + "if float(att['"+varName+"']) "+logicalOperator+" "+cmpVal
            else:
				convRules =convRules+indent + "if att['"+varName+"'] "+logicalOperator+" "+cmpVal
				
            if ans == '':
                convRules =convRules+ ":\n"
            else:
                convRules =convRules+ ":\n"+indent+" return "+ ans +"\n"
        
        self.outputStr = """
#This file was auto-generated with rulesToPy.py
class Model(object):   
 def __init__(self):
  pass
  
 def evaluate(self, att):
"""
        
        self.outputStr = self.outputStr + convRules +"""
  return False
"""
        return self.outputStr
    
