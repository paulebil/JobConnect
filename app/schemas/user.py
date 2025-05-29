from pydantic import BaseModel

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email_address: str
    password: str
    phone_number: str