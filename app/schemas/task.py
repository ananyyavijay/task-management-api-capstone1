from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

class TaskStatus(str, Enum):
    TODO = "Todo"
    IN_PROGRESS = "In progress"
    IN_REVIEW = "In Review"
    DONE = "Done"

class TaskPriority(str, Enum):
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"
    CRITICAL = "Critical"

class TaskCreateRequest(BaseModel):
    project_id: UUID = Field(...)
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.NORMAL
    assigned_to: UUID = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    assigned_to: UUID = None
    created_by: UUID
    created_at: datetime
    updated_at: datetime

class TaskUpdateRequest(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: TaskStatus | None = None
    priority: TaskPriority | None = None

class AssignTaskRequest(BaseModel):
    assigned_to: UUID