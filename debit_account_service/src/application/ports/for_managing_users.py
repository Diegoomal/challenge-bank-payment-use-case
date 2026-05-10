from abc import ABC, abstractmethod
from datetime import date

from caso_uso.src.domain.user import User


class ForManagingUsers(ABC):

    @abstractmethod
    def create_user(self, name: str, email: str, birthdate: date) -> User:
        pass

    @abstractmethod
    def list_users(self) -> list[User]:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        pass

    @abstractmethod
    def update_user(
        self,
        user_id: int,
        name: str,
        email: str,
        birthdate: date,
    ) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        pass
