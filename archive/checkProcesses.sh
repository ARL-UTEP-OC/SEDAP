#!/bin/bash
echo "******************************************************************" >> /root/coreParallelLogs.txt
echo number of logs processes: `ps auxeaf |  wc -l` >> /root/coreParallelLogs.txt
echo "$(ps ax)" >> /root/coreParallelLogs.txt
echo " " >> /root/coreParallelLogs.txt
