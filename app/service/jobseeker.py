from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.repository.jobseeker import JobSeekerProfileRepository
from app.schemas.jobseeker import JobSeekerProfileCreate
from app.models.profile import JobSeekerProfile
from app.responses.jobseeker import JobSeekerProfileResponse


class JobSeekerProfileService:
    def __init__(self, jobseeker_repository: JobSeekerProfileRepository):
        self.jobseeker_repository = jobseeker_repository

    async def create_profile(self, profile_pic: UploadFile, resume: UploadFile, data: JobSeekerProfileCreate) -> JobSeekerProfileResponse:
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
        profile = await self.jobseeker_repository.get_profile_by_user_id(user_id)
        resume_bytes = profile.resume
        return StreamingResponse(
            BytesIO(resume_bytes),
            media_type="application/pdf",
            headers={
                 "Content-Disposition": f"inline; filename=resume_{user_id}.pdf"
            }
        )

    async def get_profile_image(self, user_id: int):
        profile = await self.jobseeker_repository.get_profile_by_user_id(user_id)
        profile_pic_bytes = profile.profile_pic
        return StreamingResponse(
            BytesIO(profile_pic_bytes),
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f"inline; filename=resume_{user_id}.jpeg"
            }
        )