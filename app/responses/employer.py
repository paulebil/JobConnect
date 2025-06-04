from pydantic import BaseModel


class EmployerCompanyProfileResponse(BaseModel):
    id: int
    user_id: int
    company_name: str
    company_description: str
    company_phone: str
    location: str


    model_config = {
        "from_attributes": True
    }