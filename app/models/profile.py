from __future__ import annotations
from sqlalchemy import String, DateTime, LargeBinary, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base
from datetime import datetime
from app.utils.utc_time import utcnow

class JobSeekerProfile(Base):
    __tablename__ = "jobseeker_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    profile_pic: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    resume: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    work_experience: Mapped[int] = mapped_column(Text)
    education_level: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    user: Mapped["User"] = relationship(back_populates="jobseeker_profile")

class EmployerCompanyProfile(Base):
    __tablename__ = "employer_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    company_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    company_description: Mapped[str] = mapped_column(Text, nullable=False)
    company_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    profile_pic: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    location: Mapped[str] = mapped_column(String(100), nullable=False)

    user: Mapped["User"] = relationship(back_populates="employer_profile")
    jobs: Mapped[list["Job"]] = relationship(back_populates="employer")