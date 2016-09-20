******************

2015-11-06 (JCA)
Initial Commit

Includes all of the code that was used to generate the models for the 2012 MILCOM paper.

Ensure that CORE is installed and then run ./generateScenarios.sh

Directories are hard-coded. Must run scripts in /root/install/sedap/IntelAttacker
******************
2016-16-08 (JJM)
Second Commit

Updated for parallel execution of wireless attacks.
./generateScenarios.sh is first ran to write ALL scenarios to a text file.
May then run ./parallelScenarios.sh with file name and number of process to run at once.
******************
******************
2016-14-09 (JJM)
Third Commit

Updated comments within scripts to provide details on script responsibilities.
Sedap.sh was added for acting as a main controller for running, cleaning, 
and compressing scenarios. 

Directories are now organized, while leaving directories in root intact for now.
User may decide if they wish to delete all in root with command `rm -r [0-9]*`. 

Compressed files can be found in the OLSR OSPFv3MDR directories. 

There are now only 1680 permuatations. It is no longer possible to have the
same attacking node and victim node.
******************
