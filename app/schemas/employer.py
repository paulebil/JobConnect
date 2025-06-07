from pydantic import BaseModel, Field
from typing import Annotated

class EmployerCompanyProfileCreate(BaseModel):
    user_id: Annotated[int, Field(...)]
    company_name: Annotated[str, Field(...)]
    company_description: Annotated[str, Field(...)]
    company_phone: Annotated[str, Field(...)]
    location: Annotated[str, Field(...)]

    model_config = {
        "form_attributes": True
    }