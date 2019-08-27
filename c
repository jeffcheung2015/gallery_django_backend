#!/usr/bin/env bash

if [ "$1" = "" ] #activate
then
	source './venv/bin/activate'
elif [ "$1" = "-b" ] #start server and activate
then
  source './venv/bin/activate'
	cd backend
	python manage.py runserver 0.0.0.0:8000

elif [ "$1" = "-f" ] #start server, react and activate
then
  source './venv/bin/activate'
	cd frontend
	yarn start

elif [ "$1" = "-d" ] #deactivate
then
	deactivate
else
	echo "-b backend"
	echo "-f backend and frontend"
	echo "-d deactivate"
fi
