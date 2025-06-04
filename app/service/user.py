from fastapi import HTTPException,status
from fastapi.responses import JSONResponse

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.responses.user import UserResponse, UserDetailResponse
from app.repository.user import UserRepository

from app.core.security import hash_password, verify_password

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

    async def login_user(self, data: UserLogin) -> UserResponse:
        # Check if user exists
        user_exists = await self.user_repository.get_user_by_email(str(data.email_address))
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sign up to create an account first.")

        # Check if user password match
        password_match = verify_password(data.password, user_exists.password)
        if not password_match:
            raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user email or password.")

        user_exists.logged_in = True

        logged_in_user = await self.user_repository.update_user(user_exists)
        return UserResponse.model_validate(logged_in_user)

    async def logout_user(self,user_id: int):
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user with this id does not exists.")
        # check if user is logged in
        if not user.logged_in:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user is not logged in with us.")

        # log in the user
        user.logged_in = False
        await self.user_repository.update_user(user)
        return {"message": "user logged out successfully"}


    async def get_user_details(self, user_id: int) -> UserDetailResponse:
        # check if user exists
        user_exists = await self.user_repository.get_user_by_id(user_id)
        if not user_exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with this id does not exists.")

        # check if user is logged in
        user_logged_in = await self.user_repository.get_user_by_id(user_id)
        if not user_logged_in.logged_in:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User is not logged in to access this route.")

        return UserDetailResponse.model_validate(user_logged_in)
