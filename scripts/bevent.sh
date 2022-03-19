#!/bin/bash

OUTFILE=$1

if [ -z "$OUTFILE" ]
then
	echo "USAGE: bevent.sh OUTFILE"
	exit 1
fi

for YEAR in `(seq 1900 1 2022)`
do
	echo -e "\n\nProcessing: $YEAR"
	wine BEVENT.EXE -y $YEAR -f 0,14,34 $YEAR*.EV* >> $OUTFILE
done
