from pydantic import BaseModel, Field
from typing import Annotated

class JobCreate(BaseModel):
    employer_id: Annotated[int, Field(...)]
    title: Annotated[str, Field(..., max_length=30)]
    description: Annotated[str, Field(..., max_length=30)]
    responsibilities: Annotated[str, Field(..., max_length=20)]
    requirements: Annotated[str, Field(...)]
    location: Annotated[str, Field(..., max_length=30)]

    model_config = {
        "form_attributes": True
    }