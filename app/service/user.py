from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate
from app.responses.user import UserResponse
from app.repository.user import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, data: UserCreate) -> UserResponse:
        user_dict = data.model_dump()
        user_to_create = User(**user_dict)
        user = await self.user_repository.create_user(user_to_create)
        return UserResponse.model_validate(user)