#!/bin/sh

# Activate the virtual environment
source /venv/bin/activate
# Start the WSGI server
gunicorn --bind 0.0.0.0:5000 app:app
