set /p DATABASE_URL=<variables.txt
MOVE mapros\settings.py temp.py
MOVE local_settings.py mapros\settings.py
call python manage.py migrate
call python manage.py runserver
MOVE mapros\settings.py local_settings.py
MOVE temp.py mapros\settings.py
PAUSE
