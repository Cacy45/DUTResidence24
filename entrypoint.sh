#!/bin/sh

# Start Django
python3 ./Residence24/manage.py runserver 0.0.0.0:8000 &

# Start Nginx
nginx -g "daemon off;"