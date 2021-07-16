from uuid import UUID

from fastapi import HTTPException

from ..db import Order
from ..db.stock import StockDB, StockPriceDB
from ..models.stock import Stock, StockInDB


async def get_stock(stock_id: UUID) -> Stock:
    stock_db = await StockDB.fetch(id=stock_id)

    if not stock_db:
        raise HTTPException(404, "Stock Not Found")

    stock_db = StockInDB.parse_obj(stock_db)

    stock_price = await StockPriceDB.fetch(
        stock_id=stock_id,
        __order__=Order.desc("timestamp"),
    )

    return Stock(
        stock_id=stock_db.id,
        name=stock_db.name,
        **stock_price
    )
