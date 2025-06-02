from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)


from fastapi import Depends, Header, HTTPException
from app.repository.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_session
from app.models.user import User


async def get_current_user(user_id: int = Header(...), session: AsyncSession = Depends(get_session)) -> User:
    user_repository = UserRepository(session)
    user = await user_repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user