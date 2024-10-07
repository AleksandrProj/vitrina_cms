#!/bin/bash

exec gunicorn backend.wsgi --workers 1 --timeout 120 -b 0.0.0.0:8000