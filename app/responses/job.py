from pydantic import BaseModel
from datetime import datetime

from app.responses.employer import EmployerCompanyProfileResponse

class JobResponse(BaseModel):
    id: int
    employer_id: int
    title: str
    description: str
    responsibilities: str
    requirements: str
    location: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class JobWithEmployerResponse(BaseModel):
    id: int
    title: str
    description: str
    requirements: str
    responsibilities: str
    location: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    employer: EmployerCompanyProfileResponse

    model_config = {"from_attributes": True}