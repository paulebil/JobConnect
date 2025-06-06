from fastapi import UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from io import BytesIO

from app.repository.employer import EmployerCompanyProfileRepository
from app.schemas.employer import EmployerCompanyProfileCreate
from app.models.profile import EmployerCompanyProfile
from app.responses.employer import EmployerCompanyProfileResponse
from app.responses.dashboard import EmployerDashboard

from app.repository.user import UserRepository
from app.repository.jobseeker import JobSeekerProfileRepository
from app.repository.job import JobRepository
from app.repository.application import ApplicationRepository

from app.responses.application import ApplicationResponse, ApplicationDashboardResponse
from app.responses.job import JobResponse

class EmployerCompanyProfileService:
    def __init__(self, employer_company_profile_repository: EmployerCompanyProfileRepository, user_repository: UserRepository,
                 jobseeker_repository: JobSeekerProfileRepository, job_repository: JobRepository, application_repository: ApplicationRepository):
        self.employer_company_profile_repository = employer_company_profile_repository
        self.user_repository = user_repository
        self.jobseeker_repository = jobseeker_repository
        self.job_repository = job_repository
        self.application_repository = application_repository

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

        max_size = 10 * 1024 * 1024  # 2 MB
        if len(profile_pic_bytes) > max_size:
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

    async def get_dashboard_information(self, user_id: int):
        # Check if user exists
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id does not exist.")

        # Check if user is logged in
        if not user.logged_in:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not logged in to access this route.")

        # Get employer
        employer = await self.employer_company_profile_repository.get_profile_by_user_id(user_id)
        if not employer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employer with this user id does not exist.")

        # Get all jobs for this employer
        my_jobs = await self.job_repository.get_all_my_jobs(employer.id)
        job_response = [JobResponse.model_validate(job) for job in my_jobs]
        # print(f"Job Response: {job_response}")
        if not my_jobs:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This employer has no available job listings.")

        # Get all applications for all jobs (eager-loaded)
        my_applications = []
        for job in my_jobs:
            applications = await self.application_repository.get_all_applications_with_job_and_employer(job.id)
            application_response = [ApplicationDashboardResponse.model_validate(app) for app in applications]
            my_applications.extend(application_response)

        # Prepare response
        return EmployerDashboard(
            jobs=job_response,
            applications=my_applications,
        )
