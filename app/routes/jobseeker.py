from fastapi import APIRouter, Form, UploadFile, File, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session

from app.schemas.jobseeker import JobSeekerProfileCreate
from app.service.jobseeker import JobSeekerProfileService
from app.repository.jobseeker import JobSeekerProfileRepository

jobseeker_router = APIRouter(
    tags=["JobSeeker"]
)


def get_jobseeker_service(session: AsyncSession = Depends(get_session))-> JobSeekerProfileService:
    jobseeker_repository = JobSeekerProfileRepository(session)
    return JobSeekerProfileService(jobseeker_repository)

@jobseeker_router.post("/profile")
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