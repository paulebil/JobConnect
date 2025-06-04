from pydantic import BaseModel
from app.schemas.application import ApplicationStatus
from datetime import datetime

class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    jobseeker_id: int
    status: ApplicationStatus
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
