'''
Created on Mar 18, 2016

@author: epadilla2
'''

class Rules(object):
    '''
    classdocs
    '''
    
    def __init__(self, params):
        pass
    
    def readRules(self, filePath):
        self.filePath = filePath
        file = open(filePath)
        return file.read()
     
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
            if (cmpVal.replace('.','').replace('-','').isdigit() == False):
                cmpVal = "'" + cmpVal + "'"
            if len(elements) > 3:
                ans = elements[4]
        
            indent = ''
            for i in range(0,numTabs+1):
                indent = indent + ' '
            
            convRules =convRules+indent + "if att['"+varName+"'] "+logicalOperator+" "+cmpVal
            if ans == '':
                convRules =convRules+ ":\n"
            else:
                convRules =convRules+ ":\n"+indent+" return "+ ans +"\n"
        
        outputString = """
        #This file was auto-generated with rulesToPy.py
        class Model(object):   
         def __init__(self):
          pass
          
         def evaluate(self, att):
        """
        
        outputString = outputString + convRules +"""
          return False
        """
        
        self.pyRules = outputString
        return self.pyRules
    
    def writePy(self, text,fileName):
        text_file = open(fileName, "w")
        text_file.write(text)
        text_file.close()
    