from pydantic import BaseModel
from datetime import datetime

class JobSeekerProfileResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    phone_number: str
    years_of_experience: int
    education_level: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }