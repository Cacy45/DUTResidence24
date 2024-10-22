#!/bin/sh

# Activate the virtual environment
. /app/venv/bin/activate

# Start Django
python3 /app/Residence24/manage.py runserver 0.0.0.0:8000 &

# Start Nginx
nginx -g "daemon off;"
