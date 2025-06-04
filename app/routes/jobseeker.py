from fastapi import APIRouter, Form, UploadFile, File, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session

from app.schemas.jobseeker import JobSeekerProfileCreate
from app.service.jobseeker import JobSeekerProfileService
from app.repository.jobseeker import JobSeekerProfileRepository
from app.responses.jobseeker import JobSeekerProfileResponse

from app.repository.user import UserRepository

jobseeker_router = APIRouter(
    prefix="/jobseeker",
    tags=["JobSeeker"]
)


def get_jobseeker_service(session: AsyncSession = Depends(get_session))-> JobSeekerProfileService:
    jobseeker_repository = JobSeekerProfileRepository(session)
    user_repository = UserRepository(session)
    return JobSeekerProfileService(jobseeker_repository, user_repository)

@jobseeker_router.post("/profile", status_code=status.HTTP_201_CREATED, response_model=JobSeekerProfileResponse)
async def create_profile( first_name: str = Form(), last_name: str = Form(), phone_number: str = Form(),
                          years_of_experience: int = Form(), education_level: str = Form(), user_id: int = Form(),
                          profile_pic: UploadFile = File(), resume: UploadFile = File(),
                          jobseeker_service: JobSeekerProfileService = Depends(get_jobseeker_service)):

    data = JobSeekerProfileCreate(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        years_of_experience=years_of_experience,
        education_level=education_level
    )

    return await jobseeker_service.create_profile(profile_pic, resume, data)

@jobseeker_router.get("/profile/{user_id}/resume")
async def get_resume(user_id: int, jobseeker_service: JobSeekerProfileService = Depends(get_jobseeker_service)):
    return await jobseeker_service.get_resume(user_id)

@jobseeker_router.get("/profile/{user_id}/image")
async def get_profile_pic(user_id: int, jobseeker_service: JobSeekerProfileService = Depends(get_jobseeker_service)):
    return await jobseeker_service.get_profile_image(user_id)