from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.job import Job
from app.models.application import Application
from app.models.profile import JobSeekerProfile

class ApplicationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_application(self, application: Application):
        try:
            self.session.add(application)
            await self.session.commit()
            await self.session.refresh(application)
            return application
        except IntegrityError:
            await self.session.rollback()
            raise

    async def get_all_my_applications(self, jobseeker_id: int):
        stmt = (
            select(Application)
            .where(Application.jobseeker_id == jobseeker_id)
            .options(
                selectinload(Application.job).selectinload(Job.employer)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_applications(self) :
        stmt = (
            select(Application)
            .options(
                selectinload(Application.job).selectinload(Job.employer)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_applications_with_job_and_employer(self, job_id: int):
        stmt = (
            select(Application)
            .where(Application.job_id == job_id)
            .options(
                selectinload(Application.job).selectinload(Job.employer)
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_profiles_for_my_applications(self, employer_id: int):
        stmt = (
            select(JobSeekerProfile)
            .join(Application, Application.jobseeker_id == JobSeekerProfile.id)
            .join(Job, Job.id == Application.job_id)
            .where(Job.employer_id == employer_id)  # Filter for specific employer
        )

        result = await self.session.execute(stmt)
        jobseeker_profiles = result.scalars().all()
        return jobseeker_profiles