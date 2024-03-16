#!/bin/bash

# Stop Celery worker
pkill -f 'celery -A your_project_name worker'  # Replace your_project_name with the actual name of your Celery app

# Stop Django app (Gunicorn)
pkill -f "gunicorn task_management_system.wsgi:application"

# Stop FastAPI app (uvicorn)
pkill -f "uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001"
