from pydantic import BaseModel
from typing import List

from app.responses.application import ApplicationDashboardResponse
from app.responses.job import JobResponse



class EmployerDashboard(BaseModel):
    jobs: List[JobResponse]
    applications: List[ApplicationDashboardResponse]

    model_config = {
        "from_attributes": True
    }

