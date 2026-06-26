from sqlalchemy import DateTime, String, UUID, ForeignKey, Text, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from database import Base
import uuid

class Attachment(Base):
    __tablename__ = "attachments"

    __table_args__ = (
        Index("ix_attachments_task_id", "task_id"), 
        Index("ix_attachments_uploaded_by, uploaded_by")
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    blob_url: Mapped[str | None] = mapped_column(Text, nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size_bytes: Mapped[str] = mapped_column(String(100), nullable=False)
    uploaded_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    