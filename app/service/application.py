from app.repository.application import ApplicationRepository
from app.schemas.application import ApplicationCreate
from app.models.application import Application
from app.responses.application import ApplicationResponse

class ApplicationService:
    def __init__(self, application_repository: ApplicationRepository):
        self.application_repository = application_repository

    async def create_application(self, data: ApplicationCreate) -> ApplicationResponse:

        application = data.model_dump()
        application_to_create = Application(**application)
        created_application = await self.application_repository.create_application(application_to_create)

        return ApplicationResponse.model_validate(created_application)

