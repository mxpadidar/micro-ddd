from abc import ABC, abstractmethod

from auth.domain.entities.user import User
from shared.base import BaseRepo


class UserRepo(BaseRepo, ABC):

    def get_by_email(self, email: str) -> User:
        user = self._get_by_email(email)
        self.seen.add(user)
        return user

    @abstractmethod
    def _get_by_email(self, email: str) -> User: ...
