import os
import django

# django configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

# fastapi_app/main.py
# Define FastAPI CRUD operations for tasks using the Pydantic models
from fastapi import FastAPI, HTTPException
from django.forms.models import model_to_dict
from task.models import Task
from fastapi_app.schemas import TaskResponse, TaskListResponse, TaskCreate, TaskUpdate


app = FastAPI()

@app.get("/tasks/", response_model=TaskListResponse)
# Description: This endpoint retrieves a list of all tasks.
# Response: Returns a JSON object containing a list of tasks with their details.
# Response Model: TaskListResponse (defined in schemas.py)
# Example Usage: GET /tasks/
async def get_tasks():
    tasks = Task.objects.all()
    task_responses = [TaskResponse(**model_to_dict(task)) for task in tasks]
    return {"tasks": task_responses}


@app.post("/tasks/", response_model=TaskResponse)
# Description: This endpoint creates a new task.
# Request Body: Expects a JSON object with task details.
# Response: Returns the created task with its details.
# Response Model: TaskResponse (defined in schemas.py)
# Example Usage: POST /tasks/ with JSON body containing task details.
async def create_task(task_data: TaskCreate):
    new_task = Task.objects.create(**task_data.dict())
    return TaskResponse(**model_to_dict(new_task))


@app.put("/tasks/{task_id}/", response_model=TaskResponse)
# Description: This endpoint updates an existing task by its ID.
# Path Parameter: {task_id} (int) - ID of the task to be updated.
# Request Body: Expects a JSON object with updated task details.
# Response: Returns the updated task with its details.
# Response Model: TaskResponse (defined in schemas.py)
# Example Usage: PUT /tasks/1/ with JSON body containing updated task details.
async def update_task(task_id: int, task_data: TaskUpdate):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_data.dict(exclude_unset=True).items():
        setattr(task, field, value)
    task.save()

    updated_task_data = task_data.dict()
    updated_task_data["id"] = task_id  # Ensure the 'id' field is included
    return TaskResponse(**updated_task_data)



@app.delete("/tasks/{task_id}/")
# Description: This endpoint deletes an existing task by its ID.
# Path Parameter: {task_id} (int) - ID of the task to be deleted.
# Response: Returns a success message if the task is deleted successfully.
# Example Usage: DELETE /tasks/1/
async def delete_task(task_id: int):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        raise HTTPException(status_code=404, detail="Task not found")

    task.delete()
    return {"message": "Task deleted successfully"}

