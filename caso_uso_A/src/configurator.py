from caso_uso.src.adapters.persistence.in_memory_user_repository import (
    InMemoryUserRepository,
)
from caso_uso.src.application.ports.for_managing_users import (
    ForManagingUsers,
)
from caso_uso.src.application.services.user_management_service import UserManagementService


def configure_user_management() -> ForManagingUsers:
    repository = InMemoryUserRepository()
    return UserManagementService(repository)
