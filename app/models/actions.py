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
