from typing import List
from uuid import UUID

from fastapi import HTTPException

from ..db import Order
from ..db.stock import OwnedStockDB, StockDB, StockStreamDB
from ..models.stock import OwnedStock, Stock, StockInDB


async def get_stock(stock_id: UUID) -> Stock:
    stock_db = await StockDB.fetch_one(id=stock_id)

    if not stock_db:
        raise HTTPException(404, "Stock Not Found")

    stock_db = StockInDB.parse_obj(stock_db)

    stock_price = await StockStreamDB.fetch_one(
        stock_id=stock_id,
        __order__=Order.desc("timestamp"),
    )

    return Stock(
        name=stock_db.name,
        **stock_price
    )


async def get_owned_stock(user_id: UUID) -> List[OwnedStock]:
    owned_stock_db = await OwnedStockDB.fetch_many(user_id=user_id)

    return [OwnedStock.parse_obj(stock) for stock in owned_stock_db]
