#! /usr/bin/python

import json

data_str =  open('configuration.json','r')    
# loading json data
json_data = json.load(data_str)

# Printing data 
print "parallel execution: %s " %  json_data["parallel-executions"]
print "show-gui: %s " % json_data["show-gui"]
print "imn-template: %s " % json_data["imn-template"]["path"]
print "===> flows  <==="
print "flows per node: %s" %  json_data["flows"]["flows-per-node"]
print "wire type: %s " %  json_data["flows"]["wire-type"]
print "initial-port: %s " %  json_data["flows"]["initial-port"]
print "===> flow nodes <==="
flow_nodes =  json_data["flows"]["nodes"]
for node in flow_nodes:
	print node
print "===> outgoing-patterns <==="
outgoing_patterns =  json_data["flows"]["outgoing-patterns"]
for outgoing_pattern in outgoing_patterns:
	print "\t=== pattern ==="
	print "\trelative-node: %s" % outgoing_pattern["relative-node"]
	print "\trelative-port: %s" % outgoing_pattern["relative-port"]
	print "\tprotocol: %s" % outgoing_pattern["protocol"]
print "===> attacks <==="
attacks = json_data["attacks"]
for attack in attacks:
	print "\tname: %s" % attack["name"]
	print "\tstart-time: %s" % attack["start-time"]
	print "\tduration: %s" % attack["duration"]
	print "\tpath: %s" % attack["path"]

	print "\t=== subnets ==="
	subnets_size = attack["subnets-size"]
	for subnet_size in subnets_size: 
		print "\t", subnet_size
	print "\t=== attacker nodes ==="
	attacker_nodes = attack["attacker-nodes"]
	for node in attacker_nodes: 
		print "\t", node
	print "\t=== victim nodes ==="
	victim_nodes = attack["victim-nodes"]
	for node in victim_nodes: 
		print "\t", node
	print "===> <==="
json_str = json.dumps(json_data)
print json_str
