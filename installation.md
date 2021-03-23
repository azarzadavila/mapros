# Installation guide
This installation guide explains how to install and launch the system.
It is divised between a backend and frontend server.

## Backend
First of all, clone this repository.
### Python
The backend requires a python installation (**python >= 3.7**).
The packages contained in **requirements.txt** must be installed.
For example with *pip* it is possible to do `pip install -r requirements.txt`.
### Database
An empty Postgres database is required. Tests require the user of the database to have rights to create other databases.
The location and password of that database must be indicated in the file *variables.txt* with the following format:
`postrgres://username:password@localhost:port_number/name_of_database`

For example such database can be created through the following steps on linux :
```bash
sudo -iu postgres
createuser --interactive
createdb maprosdb
psql -d maprosdb
alter user maprosadmin with encrypted password 'localpass';
grant all privileges on database maprosdb to maprosadmin ;
alter user maprosadmin createdb ;
```
### Lean
Backend also requires an installation of Lean.
Instructions for this are available at this [link](https://leanprover-community.github.io/get_started.html).
After this, a project must be created at the root of this folder with name *lean-project* :
`leanproject new lean-project`

## Frontend
Specific on how to install the frontend are available at the frontend [repository](https://github.com/azarzadavila/mapros-frontend/installation.md).

## Running the servers
Two setting files are available one for a local configuration and another for a remote server.
By default, the remote server settings are set. 
In order to run the server on a local machine, the two files *local_settings.py* and *mapros/settings* must be swapped.
Then, an environment variable **DATABASE_URL** must be set with the content of *variables.txt*.

These two previous steps can be done by running :
* on linux or mac : `run_local.sh set`

and to restore the file after that :
* on linux or mac : `run_local.sh clean`

One can then first apply migrations and then run the server :
```bash
python manage.py migrate
python manage.py runserver
```

On windows the server can be directly started by running **run_local.bat**.