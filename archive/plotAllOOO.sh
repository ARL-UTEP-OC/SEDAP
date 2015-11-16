#!/bin/bash

for i in `ls *.mgencapture`; do cat $i  | cut -d';' -f 1,5 --output-delimiter=' ' | graph -T X -L $i; done
