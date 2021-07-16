from typing import Set
from uuid import UUID

from pydantic import BaseModel

from .stock import OwnedStock


class UserRequest(BaseModel):
    user_id: UUID


class User(UserRequest):
    name: str
    balance: float
    stoke: Set[OwnedStock]


class UserInDB(BaseModel):
    id: UUID
    name: str
    balance: float
