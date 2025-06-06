from pydantic import BaseModel, Field
from typing import Annotated

class JobSeekerProfileCreate(BaseModel):
    user_id: Annotated[int, Field(...)]
    first_name: Annotated[str, Field(..., max_length=30)]
    last_name: Annotated[str, Field(..., max_length=30)]
    phone_number: Annotated[str, Field(..., max_length=20)]
    work_experience: Annotated[str, Field(...)]
    education_level: Annotated[str, Field(...)]
    model_config = {
        "form_attributes": True
    }