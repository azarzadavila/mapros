#!/bin/bash
if [ "$1" == "set" ]; then
	export DATABASE_URL=(cat variables.txt)
	mv mapros/settings.py temp.py
	mv local_settings.py mapros/settings.py
elif [ "$1" == "clean" ]; then
	mv mapros/settings.py local_settings.py
	mv temp.py mapros/settings.py
else
	echo "Unrecognized arg"
fi
