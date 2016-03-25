
#This file was auto-generated with rulesToPy.py
class Model(object):   
 def __init__(self):
  pass
  
 def evaluate(self, att):
  if att['destSpoofed'] == 'True':
   if float(att['fromHop']) == 1:
    return True
   if float(att['fromHop']) == 2:
    if float(att['toHop']) == 1:
     if float(att['distance']) == 1:
      return False
     if float(att['distance']) == 2:
      return True
     if float(att['distance']) == 3:
      return True
     if float(att['distance']) == 4:
      return False
     if float(att['distance']) == 5:
      return False
     if float(att['distance']) == 6:
      return False
     if float(att['distance']) == 7:
      return False
     if float(att['distance']) == 8:
      return False
     if float(att['distance']) == 9:
      return False
     if float(att['distance']) == 10:
      return False
    if float(att['toHop']) == 2:
     if float(att['distance']) == 1:
      return False
     if float(att['distance']) == 2:
      if att['type'] == 'TCP':
       return True
      if att['type'] == 'UDP':
       return False
     if float(att['distance']) == 3:
      return True
     if float(att['distance']) == 4:
      return False
     if float(att['distance']) == 5:
      return False
     if float(att['distance']) == 6:
      return False
     if float(att['distance']) == 7:
      return False
     if float(att['distance']) == 8:
      return False
     if float(att['distance']) == 9:
      return False
     if float(att['distance']) == 10:
      return False
    if float(att['toHop']) == 3:
     return True
    if float(att['toHop']) == 4:
     return True
    if float(att['toHop']) == 5:
     return True
    if float(att['toHop']) == 6:
     return True
    if float(att['toHop']) == 7:
     return True
    if float(att['toHop']) == 8:
     return True
    if float(att['toHop']) == 9:
     return True
    if float(att['toHop']) == 10:
     return True
   if float(att['fromHop']) == 3:
    if float(att['toHop']) == 1:
     return True
    if float(att['toHop']) == 2:
     if float(att['distance']) == 1:
      return False
     if float(att['distance']) == 2:
      return True
     if float(att['distance']) == 3:
      return True
     if float(att['distance']) == 4:
      return False
     if float(att['distance']) == 5:
      return False
     if float(att['distance']) == 6:
      return False
     if float(att['distance']) == 7:
      return False
     if float(att['distance']) == 8:
      return False
     if float(att['distance']) == 9:
      return False
     if float(att['distance']) == 10:
      return False
    if float(att['toHop']) == 3:
     return True
    if float(att['toHop']) == 4:
     return True
    if float(att['toHop']) == 5:
     return True
    if float(att['toHop']) == 6:
     return True
    if float(att['toHop']) == 7:
     return True
    if float(att['toHop']) == 8:
     return True
    if float(att['toHop']) == 9:
     return True
    if float(att['toHop']) == 10:
     return True
   if float(att['fromHop']) == 4:
    if float(att['toHop']) == 1:
     return True
    if float(att['toHop']) == 2:
     return False
    if float(att['toHop']) == 3:
     if float(att['distance']) == 1:
      return False
     if float(att['distance']) == 2:
      return False
     if float(att['distance']) == 3:
      return True
     if float(att['distance']) == 4:
      return False
     if float(att['distance']) == 5:
      return False
     if float(att['distance']) == 6:
      return False
     if float(att['distance']) == 7:
      return False
     if float(att['distance']) == 8:
      return False
     if float(att['distance']) == 9:
      return False
     if float(att['distance']) == 10:
      return False
    if float(att['toHop']) == 4:
     return True
    if float(att['toHop']) == 5:
     return True
    if float(att['toHop']) == 6:
     return True
    if float(att['toHop']) == 7:
     return True
    if float(att['toHop']) == 8:
     return True
    if float(att['toHop']) == 9:
     return True
    if float(att['toHop']) == 10:
     return True
   if float(att['fromHop']) == 5:
    if float(att['toHop']) == 1:
     return True
    if float(att['toHop']) == 2:
     return False
    if float(att['toHop']) == 3:
     if att['type'] == 'TCP':
      return False
     if att['type'] == 'UDP':
      return True
    if float(att['toHop']) == 4:
     return False
    if float(att['toHop']) == 5:
     return True
    if float(att['toHop']) == 6:
     return True
    if float(att['toHop']) == 7:
     return True
    if float(att['toHop']) == 8:
     return True
    if float(att['toHop']) == 9:
     return True
    if float(att['toHop']) == 10:
     return True
   if float(att['fromHop']) == 6:
    if float(att['toHop']) == 1:
     return False
    if float(att['toHop']) == 2:
     return True
    if float(att['toHop']) == 3:
     return True
    if float(att['toHop']) == 4:
     return False
    if float(att['toHop']) == 5:
     return False
    if float(att['toHop']) == 6:
     return False
    if float(att['toHop']) == 7:
     return True
    if float(att['toHop']) == 8:
     return True
    if float(att['toHop']) == 9:
     return False
    if float(att['toHop']) == 10:
     return False
   if float(att['fromHop']) == 7:
    return False
   if float(att['fromHop']) == 8:
    return False
   if float(att['fromHop']) == 9:
    return False
   if float(att['fromHop']) == 10:
    return True
  if att['destSpoofed'] == 'False':
   if att['srcSpoofed'] == 'True':
    if att['type'] == 'TCP':
     if float(att['distance']) == 1:
      if float(att['toHop']) == 1:
       return True
      if float(att['toHop']) == 2:
       if float(att['fromHop']) == 1:
        return False
       if float(att['fromHop']) == 2:
        return False
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
      if float(att['toHop']) == 3:
       if float(att['fromHop']) == 1:
        return False
       if float(att['fromHop']) == 2:
        return False
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
      if float(att['toHop']) == 4:
       if float(att['fromHop']) == 1:
        return False
       if float(att['fromHop']) == 2:
        return False
       if float(att['fromHop']) == 3:
        return False
       if float(att['fromHop']) == 4:
        return False
       if float(att['fromHop']) == 5:
        return True
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
      if float(att['toHop']) == 5:
       return True
      if float(att['toHop']) == 6:
       if float(att['fromHop']) == 1:
        return False
       if float(att['fromHop']) == 2:
        return False
       if float(att['fromHop']) == 3:
        return False
       if float(att['fromHop']) == 4:
        return False
       if float(att['fromHop']) == 5:
        return False
       if float(att['fromHop']) == 6:
        return False
       if float(att['fromHop']) == 7:
        return True
       if float(att['fromHop']) == 8:
        return False
       if float(att['fromHop']) == 9:
        return False
       if float(att['fromHop']) == 10:
        return False
      if float(att['toHop']) == 7:
       return False
      if float(att['toHop']) == 8:
       return False
      if float(att['toHop']) == 9:
       return False
      if float(att['toHop']) == 10:
       return True
     if float(att['distance']) == 2:
      return True
     if float(att['distance']) == 3:
      return True
     if float(att['distance']) == 4:
      return True
     if float(att['distance']) == 5:
      return True
     if float(att['distance']) == 6:
      return True
     if float(att['distance']) == 7:
      return True
     if float(att['distance']) == 8:
      return True
     if float(att['distance']) == 9:
      return True
     if float(att['distance']) == 10:
      return True
    if att['type'] == 'UDP':
     if att['passthrough'] == 'True':
      return True
     if att['passthrough'] == 'False':
      return False
   if att['srcSpoofed'] == 'False':
    if float(att['distance']) == 1:
     return False
    if float(att['distance']) == 2:
     return False
    if float(att['distance']) == 3:
     return False
    if float(att['distance']) == 4:
     if float(att['hopsToSpoofed']) == 0:
      return False
     if float(att['hopsToSpoofed']) == 1:
      if att['passthrough'] == 'True':
       if float(att['fromHop']) == 1:
        if att['altPathWithoutAttacker'] == 'True':
         return False
        if att['altPathWithoutAttacker'] == 'False':
         return True
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
      if att['passthrough'] == 'False':
       return False
     if float(att['hopsToSpoofed']) == 2:
      return False
     if float(att['hopsToSpoofed']) == 3:
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
    if float(att['distance']) == 5:
     if float(att['hopsToSpoofed']) == 0:
      return False
     if float(att['hopsToSpoofed']) == 1:
      if att['passthrough'] == 'True':
       return True
      if att['passthrough'] == 'False':
       return False
     if float(att['hopsToSpoofed']) == 2:
      return False
     if float(att['hopsToSpoofed']) == 3:
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
    if float(att['distance']) == 6:
     return False
    if float(att['distance']) == 7:
     return False
    if float(att['distance']) == 8:
     if float(att['hopsToSpoofed']) == 0:
      return False
     if float(att['hopsToSpoofed']) == 1:
      return True
     if float(att['hopsToSpoofed']) == 2:
      return False
     if float(att['hopsToSpoofed']) == 3:
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
    if float(att['distance']) == 9:
     if float(att['hopsToSpoofed']) == 0:
      return False
     if float(att['hopsToSpoofed']) == 1:
      return True
     if float(att['hopsToSpoofed']) == 2:
      return False
     if float(att['hopsToSpoofed']) == 3:
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
    if float(att['distance']) == 10:
     return False

  return False
