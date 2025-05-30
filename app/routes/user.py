from fastapi import APIRouter, status, Depends

from app.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.responses.user import UserResponse
from app.schemas.user import UserCreate, UserLogin
from app.service.user import UserService
from app.repository.user import UserRepository

user_router = APIRouter(
    tags=["User"]
)


def get_user_service(session: AsyncSession = Depends(get_session))-> UserService:
    user_repository = UserRepository(session)
    return UserService(user_repository)

@user_router.post("/users", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def create_user( data:UserCreate, user_service: UserService =Depends( get_user_service)):
    return await user_service.create_user(data)

@user_router.post("/login", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def login_user(data: UserLogin, user_service: UserService = Depends(get_user_service)):
    return await user_service.login_user(data)

@user_router.post("/logout")
async def logout_user(user_id: int,  user_service: UserService = Depends(get_user_service)):
    return await user_service.logout_user(user_id)