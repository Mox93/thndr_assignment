from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class StockRequest(BaseModel):
    stock_id: UUID


class BaseStock(StockRequest):
    name: str
    price: float


class Stock(BaseStock):
    availability: int
    timestamp: datetime


class StockInDB(BaseModel):
    id: UUID
    name: str
