
#This file was auto-generated with rulesToPy.py
class Model(object):   
 def __init__(self):
  pass
  
 def evaluate(self, att):
  if att['passthrough'] == 'True':
   return True
  if att['passthrough'] == 'False':
   return False

  return False

