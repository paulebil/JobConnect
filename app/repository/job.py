from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.models.job import Job

class JobRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_job(self, job_to_create: Job):
        try:
            self.session.add(job_to_create)
            await self.session.commit()
            await self.session.refresh(job_to_create)
            return job_to_create
        except IntegrityError:
            await self.session.rollback()
            raise

    async def get_all_jobs(self):
        try:
            stmt = select(Job)
            result = await self.session.execute(stmt)
            jobs = result.scalars().all()
            return jobs
        except Exception:
            raise
