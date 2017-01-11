#!/bin/bash

# This script is responsible for killing all CORE services.
# Useful for when too many instances of CORE have been created or stalled.

service core-daemon stop
sleep 10s
service core-daemon start
