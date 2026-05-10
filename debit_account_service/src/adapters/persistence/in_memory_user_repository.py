from caso_uso.src.domain.user import User
from caso_uso.src.application.ports.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):

    def __init__(self):
        self.users: list[User] = []
        self.current_id = 1

    def save(self, user: User) -> User:
        user.id = self.current_id
        self.current_id += 1
        self.users.append(user)
        return user

    def find_all(self) -> list[User]:
        return self.users.copy()

    def find_by_id(self, user_id: int) -> User | None:
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def find_by_email(self, email: str) -> User | None:
        for user in self.users:
            if user.email == email:
                return user
        return None

    def update(self, user: User) -> User:
        for index, current_user in enumerate(self.users):
            if current_user.id == user.id:
                self.users[index] = user
                return user
        raise ValueError("User not found")

    def delete(self, user_id: int) -> None:
        for index, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[index]
                return
        raise ValueError("User not found")
