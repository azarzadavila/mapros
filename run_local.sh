#!/usr/bin/fish
if test "$argv[1]" = set
	export DATABASE_URL=(cat variables.txt)
	mv mapros/settings.py temp.py
	mv local_settings.py mapros/settings.py
else if test "$argv[1]" = clean
	mv mapros/settings.py local_settings.py
	mv temp.py mapros/settings.py
end
