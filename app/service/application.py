from app.repository.application import ApplicationRepository
from app.schemas.application import ApplicationCreate
from app.models.application import Application


class ApplicationService:
    def __init__(self, application_repository: ApplicationRepository):
        self.application_repository = application_repository

    async def create_application(self, data: ApplicationCreate):

        application = data.model_dump()
        application_to_create = Application(**application)

        application_to_create.jobseeker_id = 1

        await self.application_repository.create_application(application_to_create)

        return {"message": "Application created successfully"}

