from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class AttachmentRequest(BaseModel):
    pass

class AttachmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID 
    task_id: UUID
    filename: str
    blob_url: str
    content_type: str
    size_bytes: int
    uploaded_by: UUID
    uploaded_at: datetime