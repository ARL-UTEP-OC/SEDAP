The SEDAP tool enables analysts to design and execute network scenarios for several popular emulation and simulation platforms. The executed scenarios allow the generation of models that can be used to conduct multiple types of analysis. The scenarios are composed of a large number of different combinations of 1) network topologies, e.g., chain topology,  2) routing protocols, e.g., NRL OLSR, and 3) a particular type of a network attack, e.g., spoofing attack. SEDAP allows analysts to run different combinations of the aforementioned scenarios and logs scenario data such as packet arrival statistics, route states, and attack start and end times. The tool converts collected data to formats used by multiple statistical analysis tools, such as WEKA, which then generates analysis models. The generated models aid analysts to perform efficient analysis of computer networks. SEDAP also includes an analysis component that contains a visualization feature for viewing results of running statistical and comparison algorithms on node states (e.g., position of the node, and status such as compromised or not), packet transmission, and routing. The focus of this component is to facilitate the task of viewing differences between similar scenarios and the different emulation and simulation tool outputs resulting from running these scenarios.

This version of SEDAP includes all of the code that was used to generate the models for the 2012 MILCOM paper.

Ensure that CORE is installed and then run ./generateScenarios.sh

Directories are hard-coded. Must run scripts in /root/install/sedap/IntelAttacker

******************

Updated for parallel execution of wireless attacks.
./generateScenarios.sh is first ran to write ALL scenarios to a text file.
May then run ./parallelScenarios.sh with file name and number of process to run at once.

******************

Updated comments within scripts to provide details on script responsibilities.
Sedap.sh was added for acting as a main controller for running, cleaning, 
and compressing scenarios. 

Directories are now organized, while leaving directories in root intact for now.
User may decide if they wish to delete all in root with command `rm -r [0-9]*`. 

Compressed files can be found in the OLSR OSPFv3MDR directories. 

There are now only 1680 permuatations. It is no longer possible to have the
same attacking node and victim node.

May automatically run using ./sedap.sh 
Note: Text file and number of processes ran at a time are currently hard-coded.

******************
First service was created. Originally, the OLSR service was modified by.
The service has been left as it was before, and a modified version named
nrlMod.py has been made. 

To add additional services:
Go to the directory /root/.core/myservices
Add a service by file, or to an existing file by adding another class.
See README.txt for more detail. 
Note: /etc/core/core.conf has already been fixed to add custom services.


Note: You may also modify files and services within the directory
/usr/local/lib/python2.7/dist-packages/core/services
This will have the same effect as adding additional services.

Changed to use new service nrlolsrd_Mod:
blackholeAttack.sh
spoofingAttack.sh

******************

Updated comments within scripts to provide details on script responsibilities.
Sedap.sh was added for acting as a main controller for running, cleaning, 
and compressing scenarios. 

Directories are now organized, while leaving directories in root intact for now.
User may decide if they wish to delete all in root with command `rm -r [0-9]*`. 

Compressed files can be found in the OLSR OSPFv3MDR directories. 

There are now only 1680 permuatations. It is no longer possible to have the
same attacking node and victim node.

May automatically run using ./sedap.sh 
Note: Text file and number of processes ran at a time are currently hard-coded.
******************
