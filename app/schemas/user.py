from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

class UserCreate(BaseModel):
    first_name: Annotated[str, Field(..., max_length=30)]
    last_name: Annotated[str, Field(..., max_length=30)]
    email_address: Annotated[EmailStr, Field(...)]
    password: Annotated[str, Field(..., min_length=8)]
    phone_number: Annotated[str, Field(..., max_length=20)]


    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email_address: Annotated[EmailStr, Field(...)]
    password: Annotated[str, Field(..., min_length=8)]
    model_config = {
        "fom_attributes": True
    }