from typing import List
from uuid import UUID

from pydantic import BaseModel

from .stock import BaseStock


class OwnedStock(BaseStock):
    total: int


class UserRequest(BaseModel):
    user_id: UUID


class User(UserRequest):
    name: str
    balance: float
    stoke: List[OwnedStock]


class UserInDB(BaseModel):
    id: UUID
    name: str
    balance: float
