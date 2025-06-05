from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.models.profile import EmployerCompanyProfile

class EmployerCompanyProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_profile(self, profile: EmployerCompanyProfile):
        try:
            self.session.add(profile)
            await self.session.commit()
            await self.session.refresh(profile)
            return profile
        except IntegrityError:
            await self.session.rollback()
            raise

    async def get_profile_by_employer_id(self, employer_id: int) -> EmployerCompanyProfile | None:
        stmt = select(EmployerCompanyProfile).where(EmployerCompanyProfile.id == employer_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_profile_by_user_id(self, user_id: int) -> EmployerCompanyProfile | None:
        stmt = select(EmployerCompanyProfile).where(EmployerCompanyProfile.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_profile_by_company_name(self, company_name: str) -> EmployerCompanyProfile | None:
        stmt = select(EmployerCompanyProfile).where(EmployerCompanyProfile.company_name == company_name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
