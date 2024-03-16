# fastapi_app/schemas.py
# Define Pydantic schemas for FastAPI

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Schema for representing a task response
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    due_date: datetime
    priority: str
    status: str
    assigned_user_id: Optional[int] = None
    created_by_id: Optional[int] = None

    class Config:
        orm_mode = True

# Schema for representing a list of tasks in a response
class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]

# Schema for creating a new task
class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    priority: str

# Schema for updating an existing task
class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    due_date: Optional[datetime]
    priority: Optional[str]
    status: Optional[str]
    assigned_user_id: Optional[int]