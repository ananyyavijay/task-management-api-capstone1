from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.user import User

def upload_attachment(
    db: Session,
    task_id: UUID,
    file: UploadFile,
    current_user: User
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Upload attachment service not implemented."
    )


def list_attachments(
    db: Session,
    task_id: UUID,
    current_user: User
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="List attachments service not implemented.",
    )