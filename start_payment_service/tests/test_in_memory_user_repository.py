from datetime import date

import pytest

from caso_uso.src.adapters.persistence.in_memory_user_repository import (
    InMemoryUserRepository,
)
from caso_uso.src.domain.user import User


def test_save_assigns_incremental_id():
    repository = InMemoryUserRepository()

    first_user = repository.save(
        User(
            id=0,
            name="Joao",
            email="joao@email.com",
            birthdate=date(1990, 5, 20),
        )
    )
    second_user = repository.save(
        User(
            id=0,
            name="Maria",
            email="maria@email.com",
            birthdate=date(1991, 8, 10),
        )
    )

    assert first_user.id == 1
    assert second_user.id == 2


def test_find_methods_return_saved_users():
    repository = InMemoryUserRepository()
    user = repository.save(
        User(
            id=0,
            name="Joao",
            email="joao@email.com",
            birthdate=date(1990, 5, 20),
        )
    )

    assert repository.find_all() == [user]
    assert repository.find_by_id(user.id) == user
    assert repository.find_by_email(user.email) == user


def test_update_replaces_existing_user():
    repository = InMemoryUserRepository()
    user = repository.save(
        User(
            id=0,
            name="Joao",
            email="joao@email.com",
            birthdate=date(1990, 5, 20),
        )
    )
    updated_user = User(
        id=user.id,
        name="Joao Silva",
        email="joao.silva@email.com",
        birthdate=user.birthdate,
        created_at=user.created_at,
    )

    assert repository.update(updated_user) == updated_user
    assert repository.find_by_id(user.id) == updated_user


def test_update_raises_error_when_user_does_not_exist():
    repository = InMemoryUserRepository()
    user = User(
        id=999,
        name="Joao",
        email="joao@email.com",
        birthdate=date(1990, 5, 20),
    )

    with pytest.raises(ValueError, match="User not found"):
        repository.update(user)


def test_delete_removes_existing_user():
    repository = InMemoryUserRepository()
    user = repository.save(
        User(
            id=0,
            name="Joao",
            email="joao@email.com",
            birthdate=date(1990, 5, 20),
        )
    )

    repository.delete(user.id)

    assert repository.find_all() == []


def test_delete_raises_error_when_user_does_not_exist():
    repository = InMemoryUserRepository()

    with pytest.raises(ValueError, match="User not found"):
        repository.delete(999)
