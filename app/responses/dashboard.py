from pydantic import BaseModel
from datetime import datetime
from typing import List
from enum import Enum


from app.responses.application import ApplicationDashboardResponse
from app.responses.job import JobResponse
from app.responses.jobseeker import JobSeekerProfileResponse


class EmployerDashboard(BaseModel):
    jobs: List[JobResponse]
    applications: List[ApplicationDashboardResponse]

    model_config = {
        "from_attributes": True
    }



class ApplicationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class JobResponseLite(BaseModel):
    id: int
    title: str
    job_type: str
    base_salary: int
    location: str

    model_config = {
        "from_attributes": True
    }

class ApplicationWithJobSeeker(BaseModel):
    job: JobResponseLite
    jobseeker: JobSeekerProfileResponse
    status: ApplicationStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
class ApplicantsView(BaseModel):
    applicants: List[ApplicationWithJobSeeker]

