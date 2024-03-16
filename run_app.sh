#!/bin/bash

# Activate the virtual environment
source /Users/test/PycharmProjects/pythonProject/task_management_system/env/bin/activate

# Start Django app
gunicorn task_management_system.wsgi:application &

# Start FastAPI app
uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001 &

# Start Celery worker
celery -A your_project_name worker -l info &

# Deactivate the virtual environment
deactivate
