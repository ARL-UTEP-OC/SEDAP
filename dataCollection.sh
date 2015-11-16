#!/usr/bin/bash

tshark -i eth0 -T fields -E separator=, -e frame.time_epoch -e frame.len -e frame.protocols -e ip.src -e ip.dst -e ipv6.src -e ipv6.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -l
