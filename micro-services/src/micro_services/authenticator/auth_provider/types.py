from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    username: str
    password: str
    salt: str
    is_enabled: bool


class AuthProvider(metaclass=ABCMeta):

    @abstractmethod
    async def create(self, user: User) -> bool:
        ...

    @abstractmethod
    async def read(self, username: str) -> Optional[User]:
        ...

    @abstractmethod
    async def update(self, user: User) -> None:
        ...

    @abstractmethod
    async def delete(self, username: str) -> None:
        ...
