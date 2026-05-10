import re
from datetime import date


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MINIMUM_AGE = 18


def validate_email(email: str) -> None:
    if not EMAIL_PATTERN.fullmatch(email):
        raise ValueError("Invalid email")


def validate_minimum_age(
    birthdate: date,
    minimum_age: int = MINIMUM_AGE,
) -> None:
    today = date.today()
    age = today.year - birthdate.year

    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1

    if age < minimum_age:
        raise ValueError("User must be at least 18 years old")


def validate_user_data(email: str, birthdate: date) -> None:
    validate_email(email)
    validate_minimum_age(birthdate)
