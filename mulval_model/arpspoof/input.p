/*
Topology

ftpClientHost ---- subnet1 ---- router1 ---- router2 ---- ftpServer
				  /
				 /
				/
			   /
		attacker

In this scenario, the attacker takes advantage of the fact
that ftp is cleartext and conduct a MITM thanks to the use
of arp
*/

attackerLocated(subnet1).
attackGoal(execCode(ftpServerHost,userLevel)).
malicious(Attacker).

hacl(subnet1, ftpClientHost, _allProtocols , _allPorts).
hacl(subnet1, router1, _allProtocols , _allPorts).
hacl(router1, router2, _allProtocols , _allPorts).
hacl(router2, ftpServerHost, tcp , 21).

gateway(router1). 
gateway(router2). 

/* client */
clientProgram(ftpClientHost,ftpClient_app).
networkServiceInfo(ftpClientHost, arpd, _NA_layer2 , _NA_layer2 , _NA_layer2). 
vulExists(ftpClientHost, arpSpoofVuln, arpd).
vulProperty(arpSpoofVuln, remoteExploit, arpSpoof).

/* routers */
networkServiceInfo(router1 , arpd, _NA_layer2 , _NA_layer2 , _NA_layer2). 
networkServiceInfo(router2 , arpd, _NA_layer2 , _NA_layer2 , _NA_layer2). 

/* ftp server */
networkServiceInfo(ftpServerHost , ftpd, tcp , 21, userLevel). 
hasAccount(victimUser, ftpServerHost, userLevel).
networkServiceInfo(ftpServerHost, arpd, _NA_layer2 , _NA_layer2 , _NA_layer2). 
