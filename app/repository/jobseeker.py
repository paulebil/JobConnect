from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.models.profile import JobSeekerProfile

class JobSeekerProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_profile(self, profile: JobSeekerProfile):
        try:
            self.session.add(profile)
            await self.session.commit()
            await self.session.refresh(profile)
            return profile
        except IntegrityError:
            await self.session.rollback()
            raise

    async def get_profile_by_user_id(self, user_id: int) -> JobSeekerProfile | None:
        stmt = select(JobSeekerProfile).where(JobSeekerProfile.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_profile_by_jobseeker_id(self, jobseeker_id: int) -> JobSeekerProfile | None:
        stmt = select(JobSeekerProfile).where(JobSeekerProfile.id == jobseeker_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
