
#This file was auto-generated with rulesToPy.py
class Model(object):   
 def __init__(self):
  pass
  
 def evaluate(self, att):
  if att['passthrough'] == 'True':
   if att['srcSpoofed'] == 'True':
    return True
   if att['srcSpoofed'] == 'False':
    if att['destSpoofed'] == 'True':
     return True
    if att['destSpoofed'] == 'False':
     if float(att['hopsToSpoofed']) == 0:
      return False
     if float(att['hopsToSpoofed']) == 1:
      return False
     if float(att['hopsToSpoofed']) == 2:
      if float(att['fromHop']) == 1:
       return False
      if float(att['fromHop']) == 2:
       return False
      if float(att['fromHop']) == 3:
       if att['altPathWithoutAttacker'] == 'True':
        return True
       if att['altPathWithoutAttacker'] == 'False':
        return False
      if float(att['fromHop']) == 4:
       return False
      if float(att['fromHop']) == 5:
       return False
      if float(att['fromHop']) == 6:
       return True
      if float(att['fromHop']) == 7:
       return True
      if float(att['fromHop']) == 8:
       return True
      if float(att['fromHop']) == 9:
       return True
      if float(att['fromHop']) == 10:
       return False
     if float(att['hopsToSpoofed']) == 3:
      if att['altPathWithoutAttacker'] == 'True':
       if float(att['distance']) == 1:
        return False
       if float(att['distance']) == 2:
        return False
       if float(att['distance']) == 3:
        return False
       if float(att['distance']) == 4:
        return False
       if float(att['distance']) == 5:
        return True
       if float(att['distance']) == 6:
        return False
       if float(att['distance']) == 7:
        return False
       if float(att['distance']) == 8:
        return False
       if float(att['distance']) == 9:
        return True
       if float(att['distance']) == 10:
        return True
      if att['altPathWithoutAttacker'] == 'False':
       return False
     if float(att['hopsToSpoofed']) == 4:
      return False
     if float(att['hopsToSpoofed']) == 5:
      return False
     if float(att['hopsToSpoofed']) == 6:
      return False
     if float(att['hopsToSpoofed']) == 7:
      return False
     if float(att['hopsToSpoofed']) == 8:
      return False
     if float(att['hopsToSpoofed']) == 9:
      return False
     if float(att['hopsToSpoofed']) == 10:
      return False
  if att['passthrough'] == 'False':
   if att['destSpoofed'] == 'True':
    if float(att['distance']) == 1:
     return False
    if float(att['distance']) == 2:
     return False
    if float(att['distance']) == 3:
     if float(att['fromHop']) == 1:
      return False
     if float(att['fromHop']) == 2:
      return True
     if float(att['fromHop']) == 3:
      return False
     if float(att['fromHop']) == 4:
      return False
     if float(att['fromHop']) == 5:
      return False
     if float(att['fromHop']) == 6:
      return False
     if float(att['fromHop']) == 7:
      return False
     if float(att['fromHop']) == 8:
      return False
     if float(att['fromHop']) == 9:
      return False
     if float(att['fromHop']) == 10:
      return False
    if float(att['distance']) == 4:
     if float(att['fromHop']) == 1:
      return False
     if float(att['fromHop']) == 2:
      return True
     if float(att['fromHop']) == 3:
      return True
     if float(att['fromHop']) == 4:
      return False
     if float(att['fromHop']) == 5:
      return False
     if float(att['fromHop']) == 6:
      return False
     if float(att['fromHop']) == 7:
      return False
     if float(att['fromHop']) == 8:
      return False
     if float(att['fromHop']) == 9:
      return False
     if float(att['fromHop']) == 10:
      return False
    if float(att['distance']) == 5:
     if float(att['fromHop']) == 1:
      return False
     if float(att['fromHop']) == 2:
      return True
     if float(att['fromHop']) == 3:
      return True
     if float(att['fromHop']) == 4:
      return True
     if float(att['fromHop']) == 5:
      return False
     if float(att['fromHop']) == 6:
      return False
     if float(att['fromHop']) == 7:
      return False
     if float(att['fromHop']) == 8:
      return False
     if float(att['fromHop']) == 9:
      return False
     if float(att['fromHop']) == 10:
      return False
    if float(att['distance']) == 6:
     return False
    if float(att['distance']) == 7:
     return False
    if float(att['distance']) == 8:
     return False
    if float(att['distance']) == 9:
     return True
    if float(att['distance']) == 10:
     return False
   if att['destSpoofed'] == 'False':
    return False

  return False
