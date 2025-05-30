from fastapi import UploadFile, HTTPException

from app.repository.jobseeker import JobSeekerProfileRepository
from app.schemas.jobseeker import JobSeekerProfileCreate
from app.models.profile import JobSeekerProfile


class JobSeekerProfileService:
    def __init__(self, jobseeker_repository: JobSeekerProfileRepository):
        self.jobseeker_repository = jobseeker_repository

    async def create_profile(self, profile_pic: UploadFile, resume: UploadFile, data: JobSeekerProfileCreate):
        profile_pic_bytes = await profile_pic.read()
        resume_bytes = await resume.read()

        profile_to_create = data.model_dump()
        jobseeker_profile = JobSeekerProfile(**profile_to_create)

        MAX_SIZE = 10 * 1024 * 1024  # 2 MB
        if len(profile_pic_bytes) > MAX_SIZE or len(resume_bytes) > MAX_SIZE:
            raise HTTPException(status_code=400, detail="File too large.")

        jobseeker_profile.profile_pic = profile_pic_bytes
        jobseeker_profile.resume = resume_bytes

        await self.jobseeker_repository.create_profile(jobseeker_profile)

        return {"message": "Jobseeker profile created successfully"}