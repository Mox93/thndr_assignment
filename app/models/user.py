from typing import List
from uuid import UUID

from pydantic import BaseModel

from .actions import Buy, Sell
from .stock import OwnedStock


class UserRequest(BaseModel):
    user_id: UUID


class UserCreate(UserRequest):
    name: str


class User(UserCreate):
    balance: float
    stock: List[OwnedStock]
    pending_buys: List[Buy]
    pending_sells: List[Sell]


class UserInDB(BaseModel):
    id: UUID
    name: str
    balance: float
