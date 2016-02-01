attackerLocated(subnet1).
attackGoal(execCode(ftpServer,_)).
malicious(Attacker).

hacl(subnet1, ftpClient, _ , _).
hacl(subnet1, router1, _ , _).
hacl(router1, router2, _ , _).
hacl(router2, ftpServer, tcp , 20).


gateway(router1). 
gateway(router2). 

/* client */
clientProgram(ftpClient,ftpc).
networkServiceInfo(ftpClient, arpd, _protocol, _port, _).
vulExists(ftpClient, arpSpoofVuln, arpd).
vulProperty(arpSpoofVuln, remoteExploit, arpSpoof).


/* routers */
networkServiceInfo(router1 , arpd, _ , _ , _). 
networkServiceInfo(router2 , arpd, _ , _ , _). 

/* ftp server */
networkServiceInfo(ftpServer , ftpd, tcp , 20 , root). 
hasAccount(Victim, ftpServer, u).
networkServiceInfo(ftpServer , arpd, _ , _ , _). 
