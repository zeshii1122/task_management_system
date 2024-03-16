@echo off

rem Activate the virtual environment
call C:\path\to\your\virtualenv\Scripts\activate

rem Start Django app
start gunicorn task_management_system.wsgi:application

rem Start FastAPI app
start uvicorn fastapi_app.main:app --host 0.0.0.0 --port 8001

REM Start the Celery worker
start /B celery -A your_project_name worker -l info

REM Deactivate the virtual environment
deactivate