from sqlalchemy import DateTime, String, UUID, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.database import Base
import uuid
from app.database import id_type

class ProjectMember(Base):
    __tablename__ = "project_members"

    project_id: Mapped[uuid.UUID] = mapped_column(id_type, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(id_type, ForeignKey("users.id"), nullable=False, primary_key=True, index=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="member")
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))