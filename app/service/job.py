from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.repository.job import JobRepository
from app.schemas.job import JobCreate
from app.models.job import Job


class JobService:
    def __init__(self, job_repository: JobRepository):
        self.job_repository = job_repository

    async def create_job(self, data: JobCreate):

        job = data.model_dump()
        job_to_create = Job(**job)

        job_to_create.is_active = False
        job_to_create.employer_id = 1

        await self.job_repository.create_job(job_to_create)

        return {"message": "Job created successfully"}

