from fastapi import FastAPI

from .models.stock import Stock
from .db.stock import StockDB, StockStreamDB


internal = FastAPI()


@internal.post("/stock_stream")
async def add_stock_stream(info: Stock):
    stock_db = await StockDB.fetch_one(id=info.stock_id)

    if not stock_db:
        await StockDB.insert(dict(id=info.stock_id, name=info.name))

    await StockStreamDB.insert(info.dict(exclude={"name"}))
