from fastapi import FastAPI, HTTPException

from .db.stock import StockDB, StockStreamDB
from .db.user import UserDB
from .models.stock import Stock
from .models.user import UserCreate, UserInDB


internal = FastAPI()


@internal.post("/stock_stream")
async def add_stock_stream(info: Stock):
    stock_db = await StockDB.fetch_one(id=info.stock_id)

    if not stock_db:
        await StockDB.insert(dict(id=info.stock_id, name=info.name))

    await StockStreamDB.insert(info.dict(exclude={"name"}))


@internal.post("/test_user")
async def add_test_user(info: UserCreate):
    user_db = await UserDB.fetch_one(id=info.user_id)

    if user_db:
        raise HTTPException(409, "User Already Exists")

    user_db = UserInDB(id=info.user_id, name=info.name, balance=0)

    await UserDB.insert(user_db.dict())
