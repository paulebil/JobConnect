from pydantic import BaseModel, Field
from typing import Annotated

class EmployerCompanyProfileCreate(BaseModel):
    company_name: Annotated[str, Field(..., max_length=30)]
    company_description: Annotated[str, Field(..., max_length=30)]
    company_phone: Annotated[str, Field(..., max_length=20)]
    location: Annotated[str, Field(..., max_length=30)]

    model_config = {
        "form_attributes": True
    }