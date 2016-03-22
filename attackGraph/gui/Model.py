
#This file was auto-generated with rulesToPy.py
class Model(object):   
 def __init__(self):
  pass
  
 def evaluate(self, att):
  if att['passthrough'] == 'True':
   return True
  if att['passthrough'] == 'False':
   if att['distance'] == 1:
    return False
   if att['distance'] == 2:
    return False
   if att['distance'] == 3:
    if att['type'] == 'TCP':
     if att['toHop'] == 1:
      if att['fromHop'] == 1:
       return False
      if att['fromHop'] == 2:
       return True
      if att['fromHop'] == 3:
       return False
      if att['fromHop'] == 4:
       return False
      if att['fromHop'] == 5:
       return False
      if att['fromHop'] == 6:
       return False
      if att['fromHop'] == 7:
       return False
      if att['fromHop'] == 8:
       return False
      if att['fromHop'] == 9:
       return False
      if att['fromHop'] == 10:
       return False
     if att['toHop'] == 2:
      return False
     if att['toHop'] == 3:
      return False
     if att['toHop'] == 4:
      return False
     if att['toHop'] == 5:
      return False
     if att['toHop'] == 6:
      return False
     if att['toHop'] == 7:
      return False
     if att['toHop'] == 8:
      return False
     if att['toHop'] == 9:
      return False
     if att['toHop'] == 10:
      return False
    if att['type'] == 'UDP':
     return False
   if att['distance'] == 4:
    return False
   if att['distance'] == 5:
    return False
   if att['distance'] == 6:
    return False
   if att['distance'] == 7:
    return False
   if att['distance'] == 8:
    return False
   if att['distance'] == 9:
    return False
   if att['distance'] == 10:
    return False

  return False
