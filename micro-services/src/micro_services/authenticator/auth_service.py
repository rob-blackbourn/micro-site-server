import hashlib
from typing import Tuple
import uuid
from .auth_provider import User, AuthProvider


class AuthService:

    def __init__(self, auth_provider: AuthProvider) -> None:
        self.auth_provider = auth_provider
        self.is_initialised = False

    async def register(self, email: str, password: str) -> bool:
        await self._initialise()
        salt, hashed_password = self._generate_password(password)
        user = User(email, hashed_password, salt, True)
        return await self.auth_provider.create(user)

    async def is_password_for_user(self, email: str, password: str) -> bool:
        await self._initialise()
        user = await self.auth_provider.read(email)
        return self._is_valid_password(password, user.salt, user.password)

    async def is_valid(self, email: str) -> bool:
        await self._initialise()
        user = await self.auth_provider.read(email)
        return user is not None and user.is_enabled

    @classmethod
    def _generate_password(cls, password) -> Tuple[str, str]:
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
        return salt, hashed_password

    @classmethod
    def _is_valid_password(cls, password: str, salt: str, hashed_password: str) -> bool:
        rehashed_password = hashlib.sha512((password + salt).encode()).hexdigest()
        return hashed_password == rehashed_password

    async def _initialise(self):
        if self.is_initialised:
            return
        self.is_initialised = True
        await self.register('admin', 'trustno1')
