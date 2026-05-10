from datetime import date

import pytest

from caso_uso.src.adapters.persistence.in_memory_user_repository import (
    InMemoryUserRepository,
)
from caso_uso.src.application.services.user_management_service import UserManagementService


def make_user_management_service() -> UserManagementService:
    return UserManagementService(InMemoryUserRepository())


def test_list_users_returns_created_users():
    user_management = make_user_management_service()

    user = user_management.create_user(
        name="Joao",
        email="joao@email.com",
        birthdate=date(1990, 5, 20),
    )

    assert user_management.list_users() == [user]


def test_get_user_returns_user_by_id():
    user_management = make_user_management_service()

    user = user_management.create_user(
        name="Joao",
        email="joao@email.com",
        birthdate=date(1990, 5, 20),
    )

    assert user_management.get_user(user.id) == user


def test_get_user_raises_error_when_user_does_not_exist():
    user_management = make_user_management_service()

    with pytest.raises(ValueError, match="User not found"):
        user_management.get_user(999)


def test_create_user_inserts_user():
    user_management = make_user_management_service()

    birthdate = date(1990, 5, 20)
    user = user_management.create_user(
        name="Joao",
        email="joao@email.com",
        birthdate=birthdate,
    )

    assert user.id == 1
    assert user.name == "Joao"
    assert user.email == "joao@email.com"
    assert user.birthdate == birthdate


def test_create_user_raises_error_when_email_already_exists():
    user_management = make_user_management_service()
    user_management.create_user(
        name="Joao",
        email="joao@email.com",
        birthdate=date(1990, 5, 20),
    )

    with pytest.raises(ValueError, match="Email already exists"):
        user_management.create_user(
            name="Joao 2",
            email="joao@email.com",
            birthdate=date(1991, 8, 10),
        )


def test_create_user_raises_error_when_email_is_invalid():
    user_management = make_user_management_service()

    with pytest.raises(ValueError, match="Invalid email"):
        user_management.create_user(
            name="Joao",
            email="email-invalido",
            birthdate=date(1990, 5, 20),
        )


def test_create_user_raises_error_when_user_is_underage():
    user_management = make_user_management_service()

    with pytest.raises(
        ValueError,
        match="User must be at least 18 years old",
    ):
        user_management.create_user(
            name="Joao",
            email="joao@email.com",
            birthdate=date.today(),
        )


def test_update_user_changes_user_data():
    user_management = make_user_management_service()

    user = user_management.create_user(
        name="Joao",
        email="joao@email.com",
        birthdate=date(1990, 5, 20),
    )

    updated_user = user_management.update_user(
        user_id=user.id,
        name="Joao Silva",
        email="joao.silva@email.com",
        birthdate=date(1990, 5, 21),
    )

    assert updated_user.id == user.id
    assert updated_user.name == "Joao Silva"
    assert updated_user.email == "joao.silva@email.com"
    assert updated_user.birthdate == date(1990, 5, 21)
    assert user_management.get_user(user.id) == updated_user


def test_update_user_raises_error_when_user_does_not_exist():
    user_management = make_user_management_service()

    with pytest.raises(ValueError, match="User not found"):
        user_management.update_user(
            user_id=999,
            name="Joao Silva",
            email="joao.silva@email.com",
            birthdate=date(1990, 5, 21),
        )


def test_update_user_raises_error_when_email_already_exists():
    user_management = make_user_management_service()

    user_management.create_user(
        name="Joao",
        email="joao@email.com",
        birthdate=date(1990, 5, 20),
    )
    maria = user_management.create_user(
        name="Maria",
        email="maria@email.com",
        birthdate=date(1991, 8, 10),
    )

    with pytest.raises(ValueError, match="Email already exists"):
        user_management.update_user(
            user_id=maria.id,
            name="Maria Silva",
            email="joao@email.com",
            birthdate=date(1991, 8, 10),
        )


def test_update_user_raises_error_when_email_is_invalid():
    user_management = make_user_management_service()

    user = user_management.create_user(
        name="Joao",
        email="joao@email.com",
        birthdate=date(1990, 5, 20),
    )

    with pytest.raises(ValueError, match="Invalid email"):
        user_management.update_user(
            user_id=user.id,
            name="Joao Silva",
            email="email-invalido",
            birthdate=date(1990, 5, 20),
        )


def test_update_user_raises_error_when_user_is_underage():
    user_management = make_user_management_service()

    user = user_management.create_user(
        name="Joao",
        email="joao@email.com",
        birthdate=date(1990, 5, 20),
    )

    with pytest.raises(
        ValueError,
        match="User must be at least 18 years old",
    ):
        user_management.update_user(
            user_id=user.id,
            name="Joao Silva",
            email="joao.silva@email.com",
            birthdate=date.today(),
        )


def test_delete_user_removes_user():
    user_management = make_user_management_service()

    user = user_management.create_user(
        name="Joao",
        email="joao@email.com",
        birthdate=date(1990, 5, 20),
    )

    user_management.delete_user(user.id)

    assert user_management.list_users() == []


def test_delete_user_raises_error_when_user_does_not_exist():
    user_management = make_user_management_service()

    with pytest.raises(ValueError, match="User not found"):
        user_management.delete_user(999)
