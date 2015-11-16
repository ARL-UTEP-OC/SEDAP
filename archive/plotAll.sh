#!/bin/bash

for i in `ls *.mgencapture`; do cat $i  | cut -d';' -f 1,4 --output-delimiter=' ' | graph -T X -L $i; done
