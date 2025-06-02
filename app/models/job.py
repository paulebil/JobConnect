from __future__ import annotations
from sqlalchemy import String, DateTime,ForeignKey,Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from datetime import datetime
from app.utils.utc_time import utcnow

class Job(Base):
    __tablename__ = "job"

    id: Mapped[int] = mapped_column(primary_key=True)
    employer_id: Mapped[int] = mapped_column(ForeignKey("employer_profile.id"))
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(255))  # Increased length
    responsibilities: Mapped[str] = mapped_column(String(255), nullable=False)
    requirements: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    employer: Mapped["EmployerCompanyProfile"] = relationship(back_populates="jobs")