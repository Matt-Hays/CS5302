#!/bin/bash

OUTFILE=$1

if [ -z "$OUTFILE" ]
then
	echo "USAGE: bgame.sh OUTFILE"
	exit 1
fi

for YEAR in `(seq 1974 1 2019)`
do
	echo "\n\nProcessing: $YEAR"
	wine BGAME.EXE -y $YEAR -f 0,7-9,25,34-37 $YEAR* >> $OUTFILE
done
