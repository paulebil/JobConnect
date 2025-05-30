from pydantic import BaseModel, Field
from typing import Annotated

class JobSeekerProfileCreate(BaseModel):
    first_name: Annotated[str, Field(..., max_length=30)]
    last_name: Annotated[str, Field(..., max_length=30)]
    phone_number: Annotated[str, Field(..., max_length=20)]
    years_of_experience: Annotated[int, Field(...)]
    education_level: Annotated[str, Field(..., max_length=30)]
    model_config = {
        "form_attributes": True
    }