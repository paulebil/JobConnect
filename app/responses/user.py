from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email_address: str

    model_config = {
        "from_attributes": True
    }

class UserDetailResponse(UserResponse):
    logged_in: bool
    created_at: datetime
    updated_at: datetime
    model_config = {
        "from_attributes": True
    }