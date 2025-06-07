from fastapi import APIRouter, Form, UploadFile, File, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session

from app.schemas.employer import EmployerCompanyProfileCreate
from app.service.employer import EmployerCompanyProfileService
from app.repository.employer import EmployerCompanyProfileRepository
from app.responses.employer import EmployerCompanyProfileResponse

from app.repository.user import UserRepository
from app.repository.jobseeker import JobSeekerProfileRepository
from app.repository.application import ApplicationRepository
from app.repository.job import JobRepository

from app.responses.dashboard import ApplicationStatus

employer_company_profile_router = APIRouter(
    tags=["EmployerCompany"],
    prefix="/company",
)


def get_employer_company_profile_service(session: AsyncSession = Depends(get_session))-> EmployerCompanyProfileService:
    employer_company_profile_repository = EmployerCompanyProfileRepository(session)
    user_repository = UserRepository(session)
    jobseeker_profile_repository = JobSeekerProfileRepository(session)
    job_repository = JobRepository(session)
    application_repository = ApplicationRepository(session)
    return EmployerCompanyProfileService(employer_company_profile_repository, user_repository, jobseeker_profile_repository, job_repository, application_repository)


@employer_company_profile_router.post("/profile", status_code=status.HTTP_201_CREATED, response_model=EmployerCompanyProfileResponse)
async def create_profile( user_id: int = Form(), company_name: str = Form(), company_description: str = Form(), company_phone: str = Form(),
                          company_location: str = Form(), profile_pic: UploadFile = File(),
                          employer_company_profile_service: EmployerCompanyProfileService = Depends(get_employer_company_profile_service)):

    data = EmployerCompanyProfileCreate(
        user_id=user_id,
        company_name=company_name,
        company_description=company_description,
        company_phone=company_phone,
        location=company_location,
    )

    return await employer_company_profile_service.create_profile(profile_pic, data)

@employer_company_profile_router.get("/profile/{user_id}/image")
async def get_profile_pic(user_id: int, employer_company_profile_service: EmployerCompanyProfileService = Depends(get_employer_company_profile_service)):
    return await employer_company_profile_service.get_profile_image(user_id)

@employer_company_profile_router.get("/dashboard")
async def get_my_dashboard(user_id: int, employer_company_profile_service: EmployerCompanyProfileService = Depends(get_employer_company_profile_service)):
    return await employer_company_profile_service.get_dashboard_information(user_id)


@employer_company_profile_router.get("/applicants")
async def get_my_applicants_profiles(user_id: int, employer_company_profile_service: EmployerCompanyProfileService = Depends(get_employer_company_profile_service)):
    return await employer_company_profile_service.get_all_profiles_for_my_applications(user_id)

@employer_company_profile_router.get("/applicants/detail/{jobseeker_id}/{job_id}")
async def get_applicant_profile_detail(jobseeker_id: int, job_id: int, employer_company_profile_service: EmployerCompanyProfileService = Depends(get_employer_company_profile_service)):
    return await employer_company_profile_service.get_single_application_jobseeker_profile_detail(jobseeker_id, job_id)


@employer_company_profile_router.patch("/applicants/update/{jobseeker_id}/{job_id}")
async def get_applicant_profile_detail(jobseeker_id: int, job_id: int, app_status:ApplicationStatus ,  employer_company_profile_service: EmployerCompanyProfileService = Depends(get_employer_company_profile_service)):
    return await employer_company_profile_service.update_applicant_status(jobseeker_id, job_id, app_status)