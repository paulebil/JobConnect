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