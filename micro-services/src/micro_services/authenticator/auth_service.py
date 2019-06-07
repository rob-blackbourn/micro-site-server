from dataclasses import dataclass


@dataclass
class UserRecord:
    username: str
    password: str
    is_enabled: bool


class AuthService:

    def __init__(self) -> None:
        self.store = {
            'admin': UserRecord('admin', 'trustno1', True)
        }

    def register(self, email: str, password: str) -> bool:
        if email in self.store:
            return False
        self.store[email] = UserRecord(email, password, True)
        return True

    def is_password_for_user(self, email: str, password: str) -> bool:
        if email not in self.store:
            return False
        user = self.store[email]
        return user.password == password

    def is_valid(self, email: str) -> bool:
        if email not in self.store:
            return False
        user = self.store[email]
        return user.is_enabled
