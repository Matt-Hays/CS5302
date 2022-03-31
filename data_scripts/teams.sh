#!/bin/bash

OUTFILE=$1

if [ -z "$OUTFILE" ]
then
	echo "USAGE: bevent.sh OUTFILE"
	exit 1
fi

for YEAR in `(seq 1974 1 2019)`
do
	echo "Processing: $YEAR"
	sed -e 's/^/'$YEAR',/' TEAM$YEAR >> $OUTFILE
done
