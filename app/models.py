from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class Deposit(BaseModel):
    user_id: UUID
    amount: float


class Withdraw(BaseModel):
    user_id: UUID
    amount: float


class Buy(BaseModel):
    user_id: UUID
    stock_id: UUID
    total: int
    upper_bound: float
    lower_bound: float


class Sell(BaseModel):
    user_id: UUID
    stock_id: UUID
    total: int
    upper_bound: float
    lower_bound: float


class StockRequest(BaseModel):
    stock_id: UUID


class BaseStock(StockRequest):
    name: str
    price: float


class Stock(BaseStock):
    available: int
    timestamp: datetime


class OwnedStock(BaseStock):
    total: int


class UserRequest(BaseModel):
    user_id: UUID


class User(UserRequest):
    name: str
    balance: float
    stoke: List[OwnedStock]
