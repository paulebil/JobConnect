from pydantic import BaseModel, Field
from typing import Annotated

from enum import Enum

class JobType(str, Enum):
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    internship = "internship"

class JobCreate(BaseModel):
    employer_id: Annotated[int, Field(...)]
    title: Annotated[str, Field(...)]
    job_type: JobType = JobType.full_time
    base_salary: Annotated[int, Field()]
    description: Annotated[str, Field(...)]
    responsibilities: Annotated[str, Field(...)]
    requirements: Annotated[str, Field(...)]
    location: Annotated[str, Field(...)]

    model_config = {
        "form_attributes": True
    }