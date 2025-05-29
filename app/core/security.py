from app.repository.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

session = AsyncSession()
user_repository = UserRepository(session)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

async def get_current_user(user_id: int):
    current_user =  await user_repository.get_user_by_id(user_id)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not registered with us.")
    return current_user