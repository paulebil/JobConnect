from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email_address: str
    phone_number: str

    model_config = {
        "from_attributes": True
    }