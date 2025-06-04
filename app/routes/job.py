from fastapi import APIRouter, status, Depends
from typing import List

from app.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.responses.job import JobResponse
from app.schemas.job import JobCreate
from app.service.job import JobService
from app.repository.job import JobRepository

from app.repository.employer import EmployerCompanyProfileRepository
from app.repository.user import UserRepository

job_router = APIRouter(
    tags=["Jobs"],
    prefix="/Jobs",
)


def get_job_service(session: AsyncSession = Depends(get_session))-> JobService:
    job_repository = JobRepository(session)
    employer_repository = EmployerCompanyProfileRepository(session)
    user_repository = UserRepository(session)
    return JobService(job_repository, employer_repository, user_repository)

@job_router.post("/create", status_code=status.HTTP_200_OK, response_model=JobResponse)
async def create_job( data:JobCreate, job_service: JobService =Depends( get_job_service)):
    return await job_service.create_job(data)

@job_router.get("/all", status_code=status.HTTP_200_OK, response_model=List[JobResponse])
async def get_all_jobs(job_service: JobService = Depends(get_job_service)):
    return await job_service.get_all_jobs()


@job_router.get("/{job_id}", status_code=status.HTTP_200_OK, response_model=JobResponse)
async def get_job_detail(job_id: int, job_service: JobService = Depends(get_job_service)):
    return await job_service.get_job_detail(job_id)