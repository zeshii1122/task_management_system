@echo off

REM Stop Celery worker
taskkill /F /IM "celery" /T

rem Stop Django app (Gunicorn)
taskkill /IM gunicorn.exe /F

rem Stop FastAPI app (uvicorn)
taskkill /IM uvicorn.exe /F

rem Optional: Deactivate virtual environment
call C:\path\to\your\virtualenv\Scripts\deactivate.bat
