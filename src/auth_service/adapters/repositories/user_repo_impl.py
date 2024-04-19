from sqlalchemy.orm import Session

from auth_service.domain.models.user import User
from auth_service.domain.repositories.user_repo import UserRepo
from shared.exceptions import NotFoundException


class UserRepoImpl(UserRepo):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, user: User) -> None:
        self.session.add(user)

    def get(self, id: int) -> User:
        user = self.session.query(User).filter_by(id=id).first()
        if not user:
            raise NotFoundException
        return user

    def get_by_email(self, email: str) -> User:
        user = self.session.query(User).filter_by(email=email).first()
        if not user:
            raise NotFoundException
        return user