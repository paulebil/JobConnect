from fastapi import HTTPException, status
from typing import List

from app.repository.application import ApplicationRepository
from app.schemas.application import ApplicationCreate
from app.models.application import Application
from app.responses.application import ApplicationResponse

from app.repository.jobseeker import JobSeekerProfileRepository
from app.repository.user import UserRepository


class ApplicationService:
    def __init__(self, application_repository: ApplicationRepository, jobseeker_repository: JobSeekerProfileRepository,
                 user_repository: UserRepository):
        self.application_repository = application_repository
        self.jobseeker_repository = jobseeker_repository
        self.user_repository = user_repository


    async def create_application(self, data: ApplicationCreate) -> ApplicationResponse:
        # check if user is a jobseeker
        jobseeker = await self.jobseeker_repository.get_profile_by_jobseeker_id(data.jobseeker_id)
        if not jobseeker:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jobseeker with this id does not exists.")
        # check if user exists
        user_exists = await self.user_repository.get_user_by_id(jobseeker.user_id)
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id does not exists.")

        # check if user is logged in
        user_logged_in = await self.user_repository.get_user_by_id(jobseeker.user_id)
        if not user_logged_in.logged_in:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not logged in to access this route.")

        # Unpack the data into the Application Model
        application = data.model_dump()
        application_to_create = Application(**application)

        # persists the data
        created_application = await self.application_repository.create_application(application_to_create)

        return ApplicationResponse.model_validate(created_application)

    async def get_all_applications(self) -> List[ApplicationResponse]:
        applications = await self.application_repository.get_all_applications()
        if not applications:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Jobs found to display.")
        return [ApplicationResponse.model_validate(application) for application in applications]


