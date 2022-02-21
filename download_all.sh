#!/bin/bash
for wgetFile in $(ls wget*.sh)
do
	echo "running $wgetFile"
	bash $wgetFile -s
done
