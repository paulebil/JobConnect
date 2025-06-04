from app.repository.job import JobRepository
from app.schemas.job import JobCreate
from app.models.job import Job
from app.responses.job import JobResponse


class JobService:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    async def create_job(self, data: JobCreate) -> JobResponse:

        job = data.model_dump()
        job_to_create = Job(**job)

        job_to_create.is_active = False

        created_job = await self.job_repository.create_job(job_to_create)

        return JobResponse.model_validate(created_job)

