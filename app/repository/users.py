from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.users import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    async def create_user(self, user: User):
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except IntegrityError:
            self.session.rollback()
            raise
