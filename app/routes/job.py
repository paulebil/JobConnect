from fastapi import APIRouter, status, Depends

from app.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.responses.job import JobResponse
from app.schemas.job import JobCreate
from app.service.job import JobService
from app.repository.job import JobRepository

job_router = APIRouter(
    tags=["Jobs"],
    prefix="/Jobs",
)


def get_job_service(session: AsyncSession = Depends(get_session))-> JobService:
    job_repository = JobRepository(session)
    return JobService(job_repository)

@job_router.post("/create", status_code=status.HTTP_200_OK, response_model=JobResponse)
async def create_job( data:JobCreate, job_service: JobService =Depends( get_job_service)):
    return await job_service.create_job(data)
