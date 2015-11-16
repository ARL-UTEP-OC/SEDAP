#!/bin/bash

cat $1 | grep iconcoords | cut -d'{' -f2 | cut -d'}' -f 1 
