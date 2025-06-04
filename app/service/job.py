from fastapi import HTTPException, status

from app.repository.job import JobRepository
from app.schemas.job import JobCreate
from app.models.job import Job
from app.responses.job import JobResponse

from app.repository.employer import EmployerCompanyProfileRepository
from app.repository.user import UserRepository

from typing import List

class JobService:
    def __init__(self, job_repository: JobRepository, employer_repository: EmployerCompanyProfileRepository,
                 user_repository: UserRepository):
        self.job_repository = job_repository
        self.employer_repository = employer_repository
        self.user_repository = user_repository

    async def create_job(self, data: JobCreate) -> JobResponse:
        # check if employer exists
        employer_exists = await self.employer_repository.get_profile_by_employer_id(data.employer_id)
        if not employer_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Employer does not exists.")
        # check if user exists
        user_exists = await self.user_repository.get_user_by_id(employer_exists.user_id)
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id does not exists.")

        # check if user is logged in
        user_logged_in = await self.user_repository.get_user_by_id(user_exists.id)
        if not user_logged_in.logged_in:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not logged in to access this route.")

        # unpack the data to the job model
        job = data.model_dump()
        job_to_create = Job(**job)

        # persists the data
        created_job = await self.job_repository.create_job(job_to_create)

        return JobResponse.model_validate(created_job)

    async def get_all_jobs(self) -> List[JobResponse]:
        jobs = await self.job_repository.get_all_jobs()
        if not jobs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Jobs found to display.")
        return [JobResponse.model_validate(job) for job in jobs]


    async def get_job_detail(self, job_id: int) -> JobResponse:
        job = await self.job_repository.get_job_detail(job_id)
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job with this id does not exists.")

        return JobResponse.model_validate(job)

