from uuid import UUID

from pydantic import BaseModel


class Deposit(BaseModel):
    user_id: UUID
    amount: float


class Withdraw(BaseModel):
    user_id: UUID
    amount: float


class BaseTrade(BaseModel):
    stock_id: UUID
    total: int
    upper_bound: float
    lower_bound: float


class Trade(BaseTrade):
    user_id: UUID


class BuyCreate(Trade):
    pass


class Buy(BaseTrade):
    funds: float


class BuyInDB(BuyCreate, Buy):
    pass


class SellCreate(Trade):
    pass


class Sell(BaseTrade):
    pass


class SellInDB(SellCreate):
    pass
