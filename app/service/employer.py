from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.repository.employer import EmployerCompanyProfileRepository
from app.schemas.employer import EmployerCompanyProfileCreate
from app.models.profile import EmployerCompanyProfile
from app.responses.employer import EmployerCompanyProfileResponse


class EmployerCompanyProfileService:
    def __init__(self, employer_company_profile_repository: EmployerCompanyProfileRepository):
        self.employer_company_profile_repository = employer_company_profile_repository

    async def create_profile(self, profile_pic: UploadFile, data: EmployerCompanyProfileCreate) -> EmployerCompanyProfileResponse:
        profile_pic_bytes = await profile_pic.read()

        profile_to_create = data.model_dump()
        employer_company_profile = EmployerCompanyProfile(**profile_to_create)

        MAX_SIZE = 10 * 1024 * 1024  # 2 MB
        if len(profile_pic_bytes) > MAX_SIZE:
            raise HTTPException(status_code=400, detail="File too large.")

        employer_company_profile.profile_pic = profile_pic_bytes
        employer_company_profile.user_id = 6

        created_employer_profile = await self.employer_company_profile_repository.create_profile(employer_company_profile)

        return EmployerCompanyProfileResponse.model_validate(created_employer_profile)


    async def get_profile_image(self, company_id: int):
        profile = await self.employer_company_profile_repository.get_profile_by_company_id(company_id)
        profile_pic_bytes = profile.profile_pic
        return StreamingResponse(
            BytesIO(profile_pic_bytes),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f"inline; filename=resume_{company_id}.jpeg"
            }
        )