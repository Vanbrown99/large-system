from dataclasses import dataclass

from .security import hash_password


@dataclass
class User:
    id: int
    name: str
    email: str
    password_hash: str
    role: str


class UserStore:
    def __init__(self) -> None:
        self._users_by_email: dict[str, User] = {}
        self._next_id = 1

    def add(self, name: str, email: str, password: str, role: str) -> User:
        normalized_email = email.lower()
        if normalized_email in self._users_by_email:
            raise ValueError("Email is already registered")
        user = User(self._next_id, name, normalized_email, hash_password(password), role)
        self._users_by_email[normalized_email] = user
        self._next_id += 1
        return user

    def get_by_email(self, email: str) -> User | None:
        return self._users_by_email.get(email.lower())

    def get_by_id(self, user_id: str) -> User | None:
        return next((user for user in self._users_by_email.values() if str(user.id) == user_id), None)
