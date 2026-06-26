from sqlalchemy import DateTime, String, UUID, ForeignKey, Text, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from database import Base
import uuid

class Task(Base):
    __tablename__ = "tasks"

    __table_args__ = (
        # Indexes
        Index("ix_tasks_project_id", "project_id"),
        Index("ix_tasks_assigned_to", "assigned_to"),
        Index("ix_tasks_status", "status"),
        Index("ix_tasks_priority", "priority"),
        Index("ix_tasks_deleted_at", "deleted_at"),

        # Check Constraints
        CheckConstraint(
            "status IN ('Todo', 'In Progress', 'In Review', 'Done')",
            name="ck_tasks_status"
        ),
        CheckConstraint(
            "priority IN ('Low', 'Normal', 'High', 'Critical')",
            name="ck_tasks_priority"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Todo")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="Normal")
    assigned_to: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, default=None)
