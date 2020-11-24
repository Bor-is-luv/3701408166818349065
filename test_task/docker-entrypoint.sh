#!/bin/bash
sleep 5
python manage.py migrate
sleep 3
python manage.py collectstatic --noinput
sleep 3
uwsgi app.ini