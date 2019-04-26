#!/bin/bash

TKNFILE="$HOME/.shmtk"
if [ -f "$TKNFILE" ]
then
	echo "$TKNFILE found."
else
	echo "$TKNFILE not found...exiting"
	exit 1
fi

pushd shamebot/roboto/
python3.7 robocore.py $(cat $TKNFILE)
popd