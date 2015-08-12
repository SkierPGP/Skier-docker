#!/usr/bin/env bash
source /var/skier/venv/bin/activate

cd /var/skier/pyapp

gunicorn -c gunicorn_config.py app:app