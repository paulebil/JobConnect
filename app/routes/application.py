from fastapi import APIRouter, status, Depends
from typing import List

from app.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.responses.application import ApplicationResponse
from app.schemas.application import ApplicationCreate
from app.service.application import ApplicationService
from app.repository.application import ApplicationRepository

from app.repository.jobseeker import JobSeekerProfileRepository
from app.repository.user import UserRepository

application_router = APIRouter(
    tags=["Applications"],
    prefix="/application",
)


def get_application_service(session: AsyncSession = Depends(get_session))-> ApplicationService:
    application_repository = ApplicationRepository(session)
    jobseeker_repository = JobSeekerProfileRepository(session)
    user_repository = UserRepository(session)
    return ApplicationService(application_repository, jobseeker_repository, user_repository)

@application_router.post("/create", status_code=status.HTTP_200_OK, response_model=ApplicationResponse)
async def create_application( data:ApplicationCreate, application_service: ApplicationService =Depends( get_application_service)):
    return await application_service.create_application(data)

@application_router.get("/all", status_code=status.HTTP_200_OK, response_model=List[ApplicationResponse])
async def get_all_applications(application_service: ApplicationService = Depends(get_application_service)):
    return await application_service.get_all_applications()