from datetime import date

from caso_uso.src.application.ports.for_managing_users import (
    ForManagingUsers,
)


def run(user_management: ForManagingUsers) -> None:
    print("Creating user...")

    user = user_management.create_user(
        name="John",
        email="john@email.com",
        birthdate=date(1990, 5, 20),
    )

    print(f"User created: {user}")

    print("Listing users...")

    users = user_management.list_users()
    print(f"Number of users: {len(users)}")
    print(f"First user: {users[0]}")

    print("Updating user...")

    updated_user = user_management.update_user(
        user_id=user.id,
        name="John Smith",
        email="john.smith@email.com",
        birthdate=date(1990, 5, 20),
    )

    print(updated_user)
    print(user_management.get_user(user.id))

    print("Trying to create a user with an existing email...")

    try:
        user_management.create_user(
            name="John 2",
            email="john.smith@email.com",
            birthdate=date(1991, 8, 10),
        )
    except ValueError as error:
        print(f"Error: {error}")

    print("Deleting user...")

    user_management.delete_user(user.id)

    print(user_management.list_users())
