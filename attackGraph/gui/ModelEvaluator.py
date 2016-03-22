'''
Created on Mar 22, 2016

@author: epadilla2
'''
from Converter import Converter

class ModelEvaluator(Converter):
    '''
    classdocs
    '''


    def __init__(self):
        pass
    
    def writeModelEvaluationXML(self,filePath,attributes,results):
        copyAttributes = list(attributes)
        # print results
        for index, flowAttributes in enumerate(copyAttributes):
            flowAttributes["modelEvaluation"]=str(results[index])
        self.writeXML(filePath,copyAttributes)
    
    def evaluate(self, flowAttributesList):
        
        modelCode=self.readFromFile(self.filePath)
        #write to file
        text_file = open("Model.py", "w")
        text_file.write(modelCode)
        text_file.close()
        
        mod = __import__('Model', fromlist=['Model'])
        ModelClass = getattr(mod, 'Model')
        instance = ModelClass()
        
        self.evaluationResults = list()
        for flowAttributes in flowAttributesList:
            results = instance.evaluate(flowAttributes)
            self.evaluationResults.append(results)
        
        return self.evaluationResults
        