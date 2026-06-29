from fastapi import APIRouter, status, HTTPException, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.schemas.attachments import AttachmentResponse, AttachmentRequest
from app.models.user import User
from app.models.task import Task
from app.models.project import Project
from app.dependencies import get_current_user
from app.database import get_db
from uuid import UUID
from typing import List
import logging
from datetime import datetime, timezone
from app.services.blob_service import upload_attachment, list_attachments

router = APIRouter()

@router.post("/tasks/{id}/attachments", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
def upload_attachments(
    id: UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return upload_attachment(
        db=db,
        task_id=id,
        file=file,
        current_user=current_user
    )

@router.get("/tasks/{id}/attachments", response_model=list[AttachmentResponse])
def get_attachments(
    id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    return list_attachments(
        db=db,
        task_id=id,
        current_user=current_user
    )