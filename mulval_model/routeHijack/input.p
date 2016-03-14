/*
Topology

ftpClientHost -- subnet1 -- router1 -- router2 -- router3 -- ftpServer
                                          |
                                          |
                                       subnet2
                                          |
                                          |
                                       attacker

In this scenario, the attacker takes advantage of the fact
that ftp is cleartext and conducts route hijack attack thanks to 
a misconfigured routing protocol
*/

attackerLocated(subnet2).
attackGoal(execCode(ftpServerHost,userLevel)).

hacl(subnet1, ftpClientHost, _allProtocols , _allPorts).
hacl(subnet1, router1, _allProtocols , _allPorts).
hacl(router1, router2, _allProtocols , _allPorts).
hacl(subnet2, router2, _allProtocols , _allPorts).
hacl(router2, router3, _allProtocols , _allPorts).
hacl(router3, ftpServerHost, tcp , 21).

gateway(router1). 
gateway(router2).
gateway(router3).

/* client */
clientProgram(ftpClientHost,ftpClient_app).
networkServiceInfo(ftpClientHost, nrlolsr, olsr , _NA_layer3 , _NA_layer3). 
vulExists(ftpClientHost, nrlolsrVul, nrlolsr, remoteExploit, nrlolsrHijack).

/* routers */
networkServiceInfo(router1 , nrlolsr, olsr , _NA_layer3 , _NA_layer3). 
networkServiceInfo(router2 , nrlolsr, olsr , _NA_layer3 , _NA_layer3). 
networkServiceInfo(router3 , nrlolsr, olsr , _NA_layer3 , _NA_layer3). 

/* ftp server */
networkServiceInfo(ftpServerHost , ftpd, tcp , 21, userLevel). 
hasAccount(victimUser, ftpServerHost, userLevel).
networkServiceInfo(ftpServerHost, nrlolsr, olsr , _NA_layer3 , _NA_layer3). 
