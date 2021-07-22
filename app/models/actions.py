from uuid import UUID

from pydantic import BaseModel


class Deposit(BaseModel):
    user_id: UUID
    amount: float


class Withdraw(BaseModel):
    user_id: UUID
    amount: float


class Trade(BaseModel):
    user_id: UUID
    stock_id: UUID
    total: int
    upper_bound: float
    lower_bound: float


class Buy(Trade):
    pass


class BuyInDB(Buy):
    funds: float


class Sell(Trade):
    pass


class SellInDB(Sell):
    pass
