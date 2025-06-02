from sys import prefix

from fastapi import APIRouter, Form, UploadFile, File, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session

from app.schemas.employer import EmployerCompanyProfileCreate
from app.service.employer import EmployerCompanyProfileService
from app.repository.employer import EmployerCompanyProfileRepository

employer_company_profile_router = APIRouter(
    tags=["EmployerCompany"],
    prefix="/company",
)


def get_employer_company_profile_service(session: AsyncSession = Depends(get_session))-> EmployerCompanyProfileService:
    employer_company_profile_repository = EmployerCompanyProfileRepository(session)
    return EmployerCompanyProfileService(employer_company_profile_repository)

@employer_company_profile_router.post("/profile")
async def create_profile( company_name: str = Form(), company_description: str = Form(), company_phone: str = Form(),
                          company_location: str = Form(), profile_pic: UploadFile = File(),
                          employer_company_profile_service: EmployerCompanyProfileService = Depends(get_employer_company_profile_service)):

    data = EmployerCompanyProfileCreate(
        company_name=company_name,
        company_description=company_description,
        company_phone=company_phone,
        location=company_location,
    )

    return await employer_company_profile_service.create_profile(profile_pic, data)

@employer_company_profile_router.get("/profile/{user_id}/image")
async def get_profile_pic(user_id: int, employer_company_profile_service: EmployerCompanyProfileService = Depends(get_employer_company_profile_service)):
    return await employer_company_profile_service.get_profile_image(user_id)