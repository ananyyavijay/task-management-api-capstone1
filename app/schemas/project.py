from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class ProjectRequest(BaseModel):
    name: str = Field(..., min_length=3)
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    description: Optional[str]
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None