from fastapi import APIRouter, status, Depends

from app.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.responses.user import UserResponse
from app.schemas.application import ApplicationCreate
from app.service.application import ApplicationService
from app.repository.application import ApplicationRepository

application_router = APIRouter(
    tags=["Applications"],
    prefix="/application",
)


def get_application_service(session: AsyncSession = Depends(get_session))-> ApplicationService:
    application_repository = ApplicationRepository(session)
    return ApplicationService(application_repository)

@application_router.post("/create", status_code=status.HTTP_200_OK)
async def create_application( data:ApplicationCreate, application_service: ApplicationService =Depends( get_application_service)):
    return await application_service.create_application(data)