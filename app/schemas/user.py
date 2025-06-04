from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

class UserCreate(BaseModel):
    email_address: Annotated[EmailStr, Field(...)]
    password: Annotated[str, Field(..., min_length=8)]


    model_config = {
        "from_attributes": True
    }

class UserLogin(BaseModel):
    email_address: Annotated[EmailStr, Field(...)]
    password: Annotated[str, Field(..., min_length=8)]
    model_config = {
        "fom_attributes": True
    }