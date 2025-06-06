from fastapi import UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.repository.employer import EmployerCompanyProfileRepository
from app.schemas.employer import EmployerCompanyProfileCreate
from app.models.profile import EmployerCompanyProfile
from app.responses.employer import EmployerCompanyProfileResponse

from app.repository.user import UserRepository
from app.repository.jobseeker import JobSeekerProfileRepository

class EmployerCompanyProfileService:
    def __init__(self, employer_company_profile_repository: EmployerCompanyProfileRepository, user_repository: UserRepository,
                 jobseeker_repository: JobSeekerProfileRepository):
        self.employer_company_profile_repository = employer_company_profile_repository
        self.user_repository = user_repository
        self.jobseeker_repository = jobseeker_repository

    async def create_profile(self, profile_pic: UploadFile, data: EmployerCompanyProfileCreate) -> EmployerCompanyProfileResponse:
        # check if user exists
        user_exists = await self.user_repository.get_user_by_id(data.user_id)
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id does not exists.")

        # check if user is logged in
        user_logged_in = await self.user_repository.get_user_by_id(data.user_id)
        if not user_logged_in.logged_in:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not logged in to access this route.")

        # check if profile for jobseeker was already: CAN'T CREATE A EMPLOYER PROFILE IF YOU ALREADY HAVE A JOBSEEKER PROFILE
        jobseeker_profile_exists = await self.jobseeker_repository.get_profile_by_user_id(data.user_id)
        if jobseeker_profile_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't create an employer profile while you have a jobseeker profile")

        # check if profile (employer profile)exists.
        profile_exists = await self.employer_company_profile_repository.get_profile_by_user_id(data.user_id)
        if profile_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Profile for this user already exists.")

        # check if company name already exists
        company_name_exists = await self.employer_company_profile_repository.get_profile_by_company_name(data.company_name)
        if company_name_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Company name already exists.")

        profile_pic_bytes = await profile_pic.read()

        profile_to_create = data.model_dump()
        employer_company_profile = EmployerCompanyProfile(**profile_to_create)

        MAX_SIZE = 10 * 1024 * 1024  # 2 MB
        if len(profile_pic_bytes) > MAX_SIZE:
            raise HTTPException(status_code=400, detail="File too large.")

        employer_company_profile.profile_pic = profile_pic_bytes

        created_employer_profile = await self.employer_company_profile_repository.create_profile(employer_company_profile)

        return EmployerCompanyProfileResponse.model_validate(created_employer_profile)


    async def get_profile_image(self, user_id: int):
        profile = await self.employer_company_profile_repository.get_profile_by_user_id(user_id)
        profile_pic_bytes = profile.profile_pic
        return StreamingResponse(
            BytesIO(profile_pic_bytes),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f"inline; filename=resume_{user_id}.jpeg"
            }
        )