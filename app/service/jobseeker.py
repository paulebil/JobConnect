from fastapi import UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.repository.jobseeker import JobSeekerProfileRepository
from app.schemas.jobseeker import JobSeekerProfileCreate
from app.models.profile import JobSeekerProfile
from app.responses.jobseeker import JobSeekerProfileResponse

from app.repository.user import UserRepository
from app.repository.employer import EmployerCompanyProfileRepository


class JobSeekerProfileService:
    def __init__(self, jobseeker_repository: JobSeekerProfileRepository, user_repository: UserRepository,
                 employer_profile_repository: EmployerCompanyProfileRepository):
        self.jobseeker_repository = jobseeker_repository
        self.user_repository = user_repository
        self.employer_profile_repository = employer_profile_repository

    async def create_profile(self, profile_pic: UploadFile, resume: UploadFile, data: JobSeekerProfileCreate) -> JobSeekerProfileResponse:
        # check if user exists
        user_exists = await self.user_repository.get_user_by_id(data.user_id)
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id does not exists.")

        # check if user is logged in
        user_logged_in = await self.user_repository.get_user_by_id(data.user_id)
        if not user_logged_in.logged_in:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not logged in to access this route.")

        # check if profile (jobseeker profile) for this user already exists
        profile_exists = await self.jobseeker_repository.get_profile_by_user_id(data.user_id)
        if profile_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Profile for this user already exists.")

        # check if profile for employer was already created with this user_id: CAN'T CREATE A JOBSEEKER PROFILE IF YOU ALREADY HAVE A EMPLOYER PROFILE
        jobseeker_profile_exists = self.employer_profile_repository.get_profile_by_user_id(data.user_id)
        if jobseeker_profile_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can't create a jobseeker profile while you have an employer profile")

        # TODO: check if phone number exists

        profile_pic_bytes = await profile_pic.read()
        resume_bytes = await resume.read()

        profile_to_create = data.model_dump()
        jobseeker_profile = JobSeekerProfile(**profile_to_create)

        MAX_SIZE = 10 * 1024 * 1024  # 2 MB
        if len(profile_pic_bytes) > MAX_SIZE or len(resume_bytes) > MAX_SIZE:
            raise HTTPException(status_code=400, detail="File too large.")

        jobseeker_profile.profile_pic = profile_pic_bytes
        jobseeker_profile.resume = resume_bytes

        created_jobseeker = await self.jobseeker_repository.create_profile(jobseeker_profile)

        return JobSeekerProfileResponse.model_validate(created_jobseeker)

    async def get_resume(self, user_id: int):
        # check if user exists
        user_exists = await self.user_repository.get_user_by_id(user_id)
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id does not exists.")

        # check if user is logged in
        user_logged_in = await self.user_repository.get_user_by_id(user_id)
        if not user_logged_in.logged_in:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not logged in to access this route.")

        # check if profile exists.
        profile = await self.jobseeker_repository.get_profile_by_user_id(user_id)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile for this user does not exists.")

        # Retrieve the profile resume
        resume_bytes = profile.resume
        return StreamingResponse(
            BytesIO(resume_bytes),
            media_type="application/pdf",
            headers={
                 "Content-Disposition": f"inline; filename=resume_{user_id}.pdf"
            }
        )

    async def get_profile_image(self, user_id: int):
        # check if user exists
        user_exists = await self.user_repository.get_user_by_id(user_id)
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id does not exists.")

        # check if user is logged in
        user_logged_in = await self.user_repository.get_user_by_id(user_id)
        if not user_logged_in.logged_in:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not logged in to access this route.")

        # check if profile exists.
        profile = await self.jobseeker_repository.get_profile_by_user_id(user_id)
        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile for this user does not exists.")

        # Retrieve the profile image
        profile_pic_bytes = profile.profile_pic
        return StreamingResponse(
            BytesIO(profile_pic_bytes),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f"inline; filename=resume_{user_id}.jpeg"
            }
        )