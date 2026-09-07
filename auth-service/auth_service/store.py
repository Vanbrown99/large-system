from dataclasses import dataclass
import os
import time

import mysql.connector
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
        self._database_enabled = bool(os.getenv("AUTH_DB_HOST"))

    def _connection(self):
        last_error = None
        for _ in range(15):
            try:
                return mysql.connector.connect(
                    host=os.getenv("AUTH_DB_HOST", "mysql"),
                    port=int(os.getenv("AUTH_DB_PORT", "3306")),
                    database=os.getenv("AUTH_DB_NAME", "school_erp"),
                    user=os.getenv("AUTH_DB_USER", "erp_user"),
                    password=os.getenv("AUTH_DB_PASSWORD", "erp_password_change_me"),
                )
            except mysql.connector.Error as error:
                last_error = error
                time.sleep(2)
        raise RuntimeError("Authentication database is unavailable") from last_error

    def add(self, name: str, email: str, password: str, role: str) -> User:
        normalized_email = email.lower()
        if self._database_enabled:
            connection = self._connection()
            try:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                    (name, normalized_email, hash_password(password), role),
                )
                connection.commit()
                return User(cursor.lastrowid, name, normalized_email, "", role)
            except mysql.connector.IntegrityError as error:
                raise ValueError("Email is already registered") from error
            finally:
                connection.close()
        if normalized_email in self._users_by_email:
            raise ValueError("Email is already registered")
        user = User(self._next_id, name, normalized_email, hash_password(password), role)
        self._users_by_email[normalized_email] = user
        self._next_id += 1
        return user

    def get_by_email(self, email: str) -> User | None:
        if self._database_enabled:
            connection = self._connection()
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT id, name, email, password_hash, role FROM users WHERE email = %s", (email.lower(),))
                row = cursor.fetchone()
                return User(**row) if row else None
            finally:
                connection.close()
        return self._users_by_email.get(email.lower())

    def get_by_id(self, user_id: str) -> User | None:
        if self._database_enabled:
            connection = self._connection()
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT id, name, email, password_hash, role FROM users WHERE id = %s", (user_id,))
                row = cursor.fetchone()
                return User(**row) if row else None
            finally:
                connection.close()
        return next((user for user in self._users_by_email.values() if str(user.id) == user_id), None)
