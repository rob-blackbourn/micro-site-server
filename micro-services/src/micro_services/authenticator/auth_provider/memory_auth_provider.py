from typing import Optional
from .types import AuthProvider, User


class MemoryAuthProvider(AuthProvider):

    def __init__(self) -> None:
        self.store = dict()

    async def create(self, user: User) -> bool:
        if user.username in self.store:
            return False
        self.store[user.username] = user
        return True

    async def read(self, username: str) -> Optional[User]:
        return self.store.get(username)

    async def update(self, user: User) -> None:
        if user.username not in self.store:
            raise KeyError(f'Failed to find {user.username}')
        self.store[user.username] = user

    async def delete(self, username: str) -> None:
        del self.store[username]
       