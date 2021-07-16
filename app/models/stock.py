from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class StockRequest(BaseModel):
    stock_id: UUID


class BaseStock(StockRequest):
    name: str


class Stock(BaseStock):
    price: float
    availability: int
    timestamp: datetime


class OwnedStock(BaseStock):
    total: int


class StockInDB(BaseModel):
    id: UUID
    name: str
