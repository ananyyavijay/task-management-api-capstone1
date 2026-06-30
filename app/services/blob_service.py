from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.task import Task
from app.models.attachment import Attachment
from utils.blob_storage import upload_file

def upload_attachment(
    db: Session,
    task_id: UUID,
    file: UploadFile,
    current_user: User
):
    
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    
    content = file.file.read()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )
    
    blob = upload_file(
        task_id=str(task_id),
        filename=file.filename,
        content=content
    )

    attachment = Attachment(
        task_id=task_id,
        filename=file.filename,
        blob_url=blob["blob_url"],
        content_type=file.content_type or "application/octet-stream",
        size_bytes=len(content),
        uploaded_by=current_user.id,
    )

    db.add(attachment)
    db.commit()
    db.refresh(attachment)

    return attachment


def list_attachments(
    db: Session,
    task_id: UUID,
    current_user: User
):
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found."
        )
    
    attachments = (
        db.query(Attachment).filter(
            Attachment.task_id == task_id
        ).order_by(
            Attachment.uploaded_at.desc()
        ).all()
    )

    return attachments

