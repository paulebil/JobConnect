from pydantic import BaseModel, Field
from enum import Enum
from typing import Annotated

class ApplicationStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    ACCEPTED = "accepted"

class ApplicationCreate(BaseModel):
    jobseeker_id: Annotated[int, Field(...)]
    job_id: Annotated[int, Field(...)]
    status: ApplicationStatus = ApplicationStatus.PENDING
