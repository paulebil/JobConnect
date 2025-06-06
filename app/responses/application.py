from pydantic import BaseModel
from app.schemas.application import ApplicationStatus
from datetime import datetime

from app.responses.job import JobWithEmployerResponse

class ApplicationResponse(BaseModel):
    id: int
    job: JobWithEmployerResponse
    jobseeker_id: int
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class ApplicationDashboardResponse(BaseModel):
    id: int
    jobseeker_id: int
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
