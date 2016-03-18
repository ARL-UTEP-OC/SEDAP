'''
Created on Jan 1, 2016

@author: Edgar
'''
class Model(object):
    
    global hello
    
    def __init__(self):
        pass
    
    def evaluate(self, att):
        if att['destSpoofed'][0] == True:
            if att['isDstBetweenSpoofedAndAttacker'] == True:
                if att['toHop'] == 1:
                    if att['fromHop'] == 1: return False
                    if att['fromHop'] == 2: return False
                    if att['fromHop'] == 3: return True
                    if att['fromHop'] == 4: return True
                    if att['fromHop'] == 5: return True
                    if att['fromHop'] == 6: return False
                    if att['fromHop'] == 7: return False
                    if att['fromHop'] == 8: return False
                    if att['fromHop'] == 9: return True
                    if att['fromHop'] == 10: return False
                if att['toHop'] == 2: return False
                if att['toHop'] == 3: return False
                if att['toHop'] == 4: return False
                if att['toHop'] == 5: return False
                if att['toHop'] == 6: return False
                if att['toHop'] == 7: return False
                if att['toHop'] == 8: return False
                if att['toHop'] == 9: return False
                if att['toHop'] == 10: return False
            if att['isDstBetweenSpoofedAndAttacker'] == False:
                if att['fromHop'] == 1: return True
                if att['fromHop'] == 2:
                    if att['toHop'] == 1: return True
                    if att['toHop'] == 2:
                        if att['beforeDelay'] < 30.53:
                            if att['isDstBetweenSpoofedAndAttackergw'] == True: return False
                            if att['isDstBetweenSpoofedAndAttackergw'] == False: return True
                        if att['beforeDelay'] >= 30.53: return True
                    if att['toHop'] == 3: return True
                    if att['toHop'] == 4: return True
                    if att['toHop'] == 5: return True
                    if att['toHop'] == 6: return True
                    if att['toHop'] == 7: return True
                    if att['toHop'] == 8: return True
                    if att['toHop'] == 9: return True
                    if att['toHop'] == 10: return True
                if att['fromHop'] == 3: return True
                if att['fromHop'] == 4: return True
                if att['fromHop'] == 5: return True
                if att['fromHop'] == 6: return True
                if att['fromHop'] == 7: return True
                if att['fromHop'] == 8: return True
                if att['fromHop'] == 9: return True
                if att['fromHop'] == 10: return True
        if att['destSpoofed'] == False:
            if att['srcSpoofed'] == True:
                if att['type'] == "TCP":
                    if att['spoofedBetweenAttackergw'] == True: return False
                    if att['spoofedBetweenAttackergw'] == False:
                        if att['toHop'] == 1: return True
                        if att['toHop'] == 2:
                            if att['fromHop'] == 1:
                                if att['beforeDelay'] < 29.26: return False
                                if att['beforeDelay'] >= 29.26: return True
                            if att['fromHop'] == 2:
                                if att['distance'] == 1: return False
                                if att['distance'] == 2: return True
                                if att['distance'] == 3: return True
                                if att['distance'] == 4: return True
                                if att['distance'] == 5: return False
                                if att['distance'] == 6: return False
                                if att['distance'] == 7: return False
                                if att['distance'] == 8: return False
                                if att['distance'] == 9: return False
                                if att['distance'] == 10: return False
                            if att['fromHop'] == 3: return True
                            if att['fromHop'] == 4: return True
                            if att['fromHop'] == 5: return True
                            if att['fromHop'] == 6: return True
                            if att['fromHop'] == 7: return True
                            if att['fromHop'] == 8: return True
                            if att['fromHop'] == 9: return True
                            if att['fromHop'] == 10: return True
                        if att['toHop'] == 3: return True
                        if att['toHop'] == 4: return True
                        if att['toHop'] == 5: return True
                        if att['toHop'] == 6: return True
                        if att['toHop'] == 7: return True
                        if att['toHop'] == 8: return True
                        if att['toHop'] == 9: return True
                        if att['toHop'] == 10: return True
                if att['type'] == "UDP":
                    if att['passthrough'] == True:
                        if att['beforeDelay'] < 32.98:
                            if att['beforeDelay'] < 30.51: return True
                            if att['beforeDelay'] >= 30.51: return False
                        if att['beforeDelay'] >= 32.98: return True
                    if att['passthrough'] == False: return False
            if att['srcSpoofed'] == False:
                if att['distance'] == 1: return False
                if att['distance'] == 2: return False
                if att['distance'] == 3: return False
                if att['distance'] == 4:
                    if att['hopsToSpoofed'] == 0: return False
                    if att['hopsToSpoofed'] == 1:
                        if att['passthrough'] == True:
                            if att['isDstBetweenSpoofedAndAttacker'] == True: return True
                            if att['isDstBetweenSpoofedAndAttacker'] == False:
                                if att['spoofedBetweenAttackergw'] == True: return True
                                if att['spoofedBetweenAttackergw'] == False: return False
                        if att[' passthrough'] == False: return False
                    if att['hopsToSpoofed'] == 2: return False
                    if att['hopsToSpoofed'] == 3: return False
                    if att['hopsToSpoofed'] == 4: return False
                    if att['hopsToSpoofed'] == 5: return False
                    if att['hopsToSpoofed'] == 6: return False
                    if att['hopsToSpoofed'] == 7: return False
                    if att['hopsToSpoofed'] == 8: return False
                    if att['hopsToSpoofed'] == 9: return False
                    if att['hopsToSpoofed']== 10: return False
                if att['distance'] == 5:
                    if att['hopsToSpoofed'] == 0: return False
                    if att['hopsToSpoofed'] == 1:
                        if att['passthrough'] == True:
                            if att['isDstBetweenSpoofedAndAttacker'] == True: return True
                            if att['isDstBetweenSpoofedAndAttacker'] == False:
                                if att['spoofedBetweenAttacker'] == True: return False
                                if att['spoofedBetweenAttacker'] == False: return True
                        if att['passthrough'] == False: return False
                    if att['hopsToSpoofed'] == 2: return False
                    if att['hopsToSpoofed'] == 3: return False
                    if att['hopsToSpoofed'] == 4: return False
                    if att['hopsToSpoofed'] == 5: return False
                    if att['hopsToSpoofed'] == 6: return False
                    if att['hopsToSpoofed'] == 7: return False
                    if att['hopsToSpoofed'] == 8: return False
                    if att['hopsToSpoofed'] == 9: return False
                    if att['hopsToSpoofed'] == 10: return False
                if att['distance'] == 6: return False
                if att['distance'] == 7: return False
                if att['distance'] == 8:
                    if att['hopsToSpoofed'] == 0: return False
                    if att['hopsToSpoofed'] == 1: return True
                    if att['hopsToSpoofed'] == 2: return False
                    if att['hopsToSpoofed'] == 3: return False
                    if att['hopsToSpoofed'] == 4: return False
                    if att['hopsToSpoofed'] == 5: return False
                    if att['hopsToSpoofed'] == 6: return False
                    if att['hopsToSpoofed'] == 7: return False
                    if att['hopsToSpoofed'] == 8: return False
                    if att['hopsToSpoofed'] == 9: return False
                    if att['hopsToSpoofed'] == 10: return False
                if att['distance'] == 9:
                    if att['hopsToSpoofed'] == 0: return False
                    if att['hopsToSpoofed'] == 1: return True
                    if att['hopsToSpoofed'] == 2: return False
                    if att['hopsToSpoofed'] == 3: return False
                    if att['hopsToSpoofed'] == 4: return False
                    if att['hopsToSpoofed'] == 5: return False
                    if att['hopsToSpoofed'] == 6: return False
                    if att['hopsToSpoofed'] == 7: return False
                    if att['hopsToSpoofed'] == 8: return False
                    if att['hopsToSpoofed'] == 9: return False
                    if att['hopsToSpoofed'] == 10: return False
                if att['distance'] == 10: return False
        return False