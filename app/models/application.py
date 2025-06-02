from __future__ import annotations
from sqlalchemy import String, DateTime,ForeignKey,Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLAlchemyEnum

from app.database.database import Base
from app.schemas.application import ApplicationStatus
from datetime import datetime
from app.utils.utc_time import utcnow

class Application(Base):
    __tablename__ = "application"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("job.id"))
    jobseeker_id: Mapped[int] = mapped_column(ForeignKey("jobseeker_profile.id"))

    status: Mapped[ApplicationStatus] = mapped_column(SQLAlchemyEnum(ApplicationStatus, name="application_status"),
                                                      default=ApplicationStatus.PENDING)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    job: Mapped["Job"] = relationship(back_populates="applications")
    jobseeker: Mapped["JobSeekerProfile"] = relationship()




