#!/bin/bash

# This script is responsible for generating res.arff files within a 
# scenario folder and an all.arff file within its parent folder. 
# Is also used to validate contents of wireless attacks and wired 
# attacks (successfulAttack.py)
# Note: Generated res.arffs are currently used for scenario integrity 
# validation within the cleaScenarios.sh script.

# NOTE: WEKA rules may have to change based on attackNodeNum->attackNodeIP (0_0_0_0 FORMAT) ********8

arffDir=$1
scriptDir=`pwd`

cd $arffDir

if [ -f all.arff ]; then
    rm all.arff
fi

#write header here
#instance += str(flow[0])+","+str(fromHop)+","+str(toHop)+","+str(type)+","+str(dist)+","+str(passThrough)+","+str(beforeDelay)+","+str(beforeMissed)+","+str(beforeOOO)+","+str(beforeNumPackets)+","+str(duringDelay)+","+str(duringMissed)+","+str(duringOOO)+","+str(duringNumPackets)+","+str(afterDelay)+","+str(afterMissed)+","+str(afterOOO)+","+str(afterNumPackets)+","+destIsSpoofed+","+str(attackName)
echo "@relation manet" > all.arff
echo "@attribute path string" >> all.arff
echo "@attribute attackNodeIP string" >> all.arff
echo "@attribute description string" >> all.arff
echo "@attribute fromHop {1,2,3,4,5,6,7,8,9,10}" >> all.arff
echo "@attribute toHop {1,2,3,4,5,6,7,8,9,10}" >> all.arff
echo "@attribute type {TCP,UDP}" >> all.arff
echo "@attribute distance {1,2,3,4,5,6,7,8,9,10}" >> all.arff
echo "@attribute passthrough {true, false}" >> all.arff
echo "@attribute beforeDelay numeric" >> all.arff
echo "@attribute beforeMissed numeric" >> all.arff
echo "@attribute beforeOOO numeric" >> all.arff
echo "@attribute beforeNumPackets numeric" >> all.arff
echo "@attribute duringDelay numeric" >> all.arff
echo "@attribute duringMissed numeric" >> all.arff
echo "@attribute duringOOO numeric" >> all.arff
echo "@attribute duringNumPackets numeric" >> all.arff
echo "@attribute afterDelay numeric" >> all.arff
echo "@attribute afterMissed numeric" >> all.arff
echo "@attribute afterOOO numeric" >> all.arff
echo "@attribute afterNumPackets numeric" >> all.arff
echo "@attribute srcSpoofed {true, false}" >> all.arff
echo "@attribute destSpoofed {true, false}" >> all.arff
echo "@attribute hopsToSpoofed {0,1,2,3,4,5,6,7,8,9,10}" >> all.arff
echo "@attribute duringLinkLost {true, false}" >> all.arff
echo "@attribute afterLinkLost {true, false}" >> all.arff
echo "@attribute attackName string" >> all.arff
echo "@attribute hopsFromSpoofedToDest numeric" >> all.arff
echo "@attribute attackerCloserToDestThanSpoofed {true, false}" >> all.arff
echo "@attribute spoofedBetweenAttacker {true, false}" >> all.arff
echo "@attribute isDstBetweenSpoofedAndAttacker {true, false}" >> all.arff
echo "@attribute spoofedBetweenAttackergw {true, false}" >> all.arff
echo "@attribute isDstBetweenSpoofedAndAttackergw {true, false}" >> all.arff
echo "@attribute isAttackerBetweenSpoofedAndDst {true, false}" >> all.arff
echo "@attribute isAttackerBetweenSpoofedAndDstgw {true, false}" >> all.arff
echo "@attribute isSrcBetweenSpoofedAndDst {true, false}" >> all.arff
echo "@attribute isSrcBetweenSpoofedAndDstgw {true, false}" >> all.arff
echo "@attribute altPathWithoutAttacker {true, false}" >> all.arff
echo "@data" >> "all.arff"

#traverse through each directory within the current directory
for dir in `ls -d */`; do
	
	if [[ $dir == *"_sh"* ]]
	then
		cd $dir
		echo "inside $dir"

		echo "@relation manet" > res.arff
		echo "@attribute path string" >> res.arff
		echo "@attribute attackNodeNum {1,2,3,4,5,6,7,8,9,10}" >> res.arff
		echo "@attribute description string" >> res.arff
		echo "@attribute fromHop {1,2,3,4,5,6,7,8,9,10}" >> res.arff
		echo "@attribute toHop {1,2,3,4,5,6,7,8,9,10}" >> res.arff
		echo "@attribute type {TCP,UDP}" >> res.arff
		echo "@attribute distance {1,2,3,4,5,6,7,8,9,10}" >> res.arff
		echo "@attribute passthrough {true, false}" >> res.arff
		echo "@attribute beforeDelay numeric" >> res.arff
		echo "@attribute beforeMissed numeric" >> res.arff
		echo "@attribute beforeOOO numeric" >> res.arff
		echo "@attribute beforeNumPackets numeric" >> res.arff
		echo "@attribute duringDelay numeric" >> res.arff
		echo "@attribute duringMissed numeric" >> res.arff
		echo "@attribute duringOOO numeric" >> res.arff
		echo "@attribute duringNumPackets numeric" >> res.arff
		echo "@attribute afterDelay numeric" >> res.arff
		echo "@attribute afterMissed numeric" >> res.arff
		echo "@attribute afterOOO numeric" >> res.arff
		echo "@attribute afterNumPackets numeric" >> res.arff
		echo "@attribute srcSpoofed {true, false}" >> res.arff
		echo "@attribute destSpoofed {true, false}" >> res.arff
		echo "@attribute hopsToSpoofed {0,1,2,3,4,5,6,7,8,9,10}" >> res.arff
		echo "@attribute duringLinkLost {true, false}" >> res.arff
		echo "@attribute afterLinkLost {true, false}" >> res.arff
		echo "@attribute attackName string" >> res.arff
		echo "@attribute hopsFromSpoofedToDest numeric" >> res.arff
		echo "@attribute attackerCloserToDestThanSpoofed {true, false}" >> res.arff
		echo "@attribute spoofedBetweenAttacker {true, false}" >> res.arff
		echo "@attribute isDstBetweenSpoofedAndAttacker {true, false}" >> res.arff
		echo "@attribute spoofedBetweenAttackergw {true, false}" >> res.arff
		echo "@attribute isDstBetweenSpoofedAndAttackergw {true, false}" >> res.arff
		echo "@attribute isAttackerBetweenSpoofedAndDst {true, false}" >> res.arff
		echo "@attribute isAttackerBetweenSpoofedAndDstgw {true, false}" >> res.arff
		echo "@attribute isSrcBetweenSpoofedAndDst {true, false}" >> res.arff
		echo "@attribute isSrcBetweenSpoofedAndDstgw {true, false}" >> res.arff
		echo "@attribute altPathWithoutAttacker {true, false}" >> res.arff
		echo "@data" >> res.arff

		attackerIP=`ls | grep capture | grep -v mgen | cut -d'.' -f1`
		$scriptDir/netStateBuilder.py 30 30 $attackerIP >> res.arff
		$scriptDir/netStateBuilder.py 30 30 $attackerIP >> ../all.arff

		cd ../
	fi
done
