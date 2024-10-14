#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput --clear
python manage.py update_index
exec gunicorn backend.wsgi --workers 1 --timeout 120 -b 0.0.0.0:8010