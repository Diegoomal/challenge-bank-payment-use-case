from datetime import date, datetime

from caso_uso.src.domain.user import User
from caso_uso.src.application.ports.user_repository import UserRepository
from caso_uso.src.application.ports.for_managing_users import (
    ForManagingUsers,
)
from caso_uso.src.application.services.user_validations import validate_user_data


class UserManagementService(ForManagingUsers):

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, name: str, email: str, birthdate: date) -> User:
        validate_user_data(email, birthdate)

        existing_user = self.repository.find_by_email(email)

        if existing_user:
            raise ValueError("Email already exists")

        user = User(id=0, name=name, email=email, birthdate=birthdate)

        return self.repository.save(user)

    def list_users(self) -> list[User]:
        return self.repository.find_all()

    def get_user(self, user_id: int) -> User:
        user = self.repository.find_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        return user

    def update_user(
        self,
        user_id: int,
        name: str,
        email: str,
        birthdate: date,
    ) -> User:
        user = self.repository.find_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        existing_user = self.repository.find_by_email(email)

        if existing_user and existing_user.id != user_id:
            raise ValueError("Email already exists")

        validate_user_data(email, birthdate)

        updated_user = User(
            id=user_id,
            name=name,
            email=email,
            birthdate=birthdate,
            created_at=user.created_at,
            updated_at=datetime.now(),
        )

        return self.repository.update(updated_user)

    def delete_user(self, user_id: int) -> None:
        user = self.repository.find_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        self.repository.delete(user_id)
