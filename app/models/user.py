from __future__ import annotations
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from datetime import datetime
from app.utils.utc_time import utcnow

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    logged_in: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    jobseeker_profile: Mapped["JobSeekerProfile"] = relationship(back_populates="user", uselist=False)
    employer_profile: Mapped["EmployerCompanyProfile"] = relationship(back_populates="user", uselist=False)
