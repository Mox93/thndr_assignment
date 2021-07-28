from datetime import datetime, timedelta
from typing import List, Union
from uuid import UUID

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException

from ..db import All, Order, Ge, Le
from ..db.stock import OwnedStockDB, StockDB, StockStreamDB
from ..models.stock import (
    OwnedStock,
    Stock,
    StockDuration,
    StockInDB,
    StockRequest,
    Duration,
)


DURATION_MAP = {
    Duration.hour: lambda now: All(
        Ge(now - timedelta(hours=1)),
        Le(now)
    ),
    Duration.day: lambda now: All(
        Ge(now - timedelta(days=1)),
        Le(now)
    ),
    Duration.week: lambda now: All(
        Ge(now - timedelta(weeks=1)),
        Le(now)
    ),
    Duration.month: lambda now: All(
        Ge(now - relativedelta(months=1)),
        Le(now)
    ),
    Duration.year: lambda now: All(
        Ge(now - relativedelta(years=1)),
        Le(now)
    ),
}


async def get_stock(info: StockRequest) -> Union[Stock, StockDuration]:
    stock_db = await StockDB.fetch_one(id=info.stock_id)

    if not stock_db:
        raise HTTPException(404, "Stock Not Found")

    stock_db = StockInDB.parse_obj(stock_db)

    stock_price = await StockStreamDB.fetch_one(
        stock_id=info.stock_id,
        __order__=Order.desc("timestamp"),
    )

    current = Stock(name=stock_db.name, **stock_price)

    if info.duration:
        high = await StockStreamDB.fetch_one(
            stock_id=info.stock_id,
            timestamp=DURATION_MAP[info.duration](datetime.utcnow()),
            __order__=Order.desc("price"),
        )
        low = await StockStreamDB.fetch_one(
            stock_id=info.stock_id,
            timestamp=DURATION_MAP[info.duration](datetime.utcnow()),
            __order__=Order.asc("price"),
        )

        return StockDuration(
            current=current,
            high=Stock(name=stock_db.name, **high),
            low=Stock(name=stock_db.name, **low),
        )

    return current


async def get_owned_stock(user_id: UUID) -> List[OwnedStock]:
    owned_stock_db = await OwnedStockDB.fetch_many(user_id=user_id)

    return [OwnedStock.parse_obj(stock) for stock in owned_stock_db]
