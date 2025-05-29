from fastapi import HTTPException,status

from app.models.user import User
from app.schemas.user import UserCreate
from app.responses.user import UserResponse
from app.repository.user import UserRepository

from app.core.security import hash_password

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, data: UserCreate) -> UserResponse:
        # Check if user exists
        user_exists = await self.user_repository.get_user_by_email(str(data.email_address))
        if user_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists.")
        # Hash user password
        hashed_password = hash_password(data.password)
        data.password = hashed_password
        print(data.password)
        user_dict = data.model_dump()
        user_to_create = User(**user_dict)
        user = await self.user_repository.create_user(user_to_create)
        return UserResponse.model_validate(user)