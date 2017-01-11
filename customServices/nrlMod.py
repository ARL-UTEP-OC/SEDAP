#
# CORE
#
# author: Jesus Medrano, Jaime Acosta
#
'''
nrlMod.py: defines services provided by ARL:
Modified version of nrl.py to allow multiple OLSR scenarios to be ran at once
'''

from core.service import CoreService, addservice
from core.misc.ipaddr import IPv4Prefix, IPv6Prefix
from core.misc.utils import *
from core.constants import *

class NrlServiceMod(CoreService):
    ''' Parent class for NRL services. Defines properties and methods
        common to NRL's routing daemons.
    '''
    _name = "ProteanMod"
    _group = "ProtoSvcMod"
    _depends = ()
    _dirs = ()
    _configs = ()
    _startindex = 45
    _startup = ()
    _shutdown = ()

    @classmethod
    def generateconfig(cls,  node, filename, services):
        return ""
        
    @staticmethod
    def firstipv4prefix(node, prefixlen=24):
        ''' Similar to QuaggaService.routerid(). Helper to return the first IPv4
        prefix of a node, using the supplied prefix length. This ignores the
        interface's prefix length, so e.g. '/32' can turn into '/24'.
        '''
        for ifc in node.netifs():
            if hasattr(ifc, 'control') and ifc.control == True:
                continue
            for a in ifc.addrlist:
                if a.find(".") >= 0:
                    addr = a.split('/')[0]
                    pre = IPv4Prefix("%s/%s" % (addr, prefixlen))
                    return str(pre)
        #raise ValueError,  "no IPv4 address found"
        return "0.0.0.0/%s" % prefixlen

class NrlOlsrMod(NrlServiceMod):
    ''' Optimized Link State Routing protocol for MANET networks.
    '''
    _name = "OLSR_Mod"
    _startup = ("nrlolsrd_Mod", )
    _shutdown = ("killall nrlolsrd_Mod", )
    _validate = ("pidof nrlolsrd_Mod", )
    
    @classmethod
    def getstartup(cls,  node,  services):
        ''' Generate the appropriate command-line based on node interfaces.
        '''
        cmd = cls._startup[0]
        netifs = list(node.netifs())
        if len(netifs) > 0:
            ifc = netifs[0]
            cmd += " -i %s" % ifc.name
        cmd += " -l /var/log/nrlolsrd_Mod.log"

        servicenames = map(lambda x: x._name,  services)
        if "SMF" in servicenames and not "NHDP" in servicenames:
            cmd += " -flooding s-mpr"
            cmd += " -smfClient %s_smf" % node.name
        if "zebra" in servicenames:
            cmd += " -z"

        return (cmd, )
        
addservice(NrlOlsrMod)
