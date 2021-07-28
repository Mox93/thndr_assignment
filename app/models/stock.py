from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Duration(str, Enum):
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class BaseStock(BaseModel):
    stock_id: UUID


class StockRequest(BaseStock):
    duration: Duration = None


class NamedStock(BaseStock):
    name: str


class Stock(NamedStock):
    price: float
    availability: int
    timestamp: datetime


class StockDuration(BaseModel):
    current: Stock
    high: Stock
    low: Stock


class OwnedStock(NamedStock):
    total: int


class StockInDB(BaseModel):
    id: UUID
    name: str
