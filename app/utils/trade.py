from fastapi import HTTPException

from .funds import add_funds, remove_funds
from .stock import get_stock
from .user import get_user
from ..db.stock import OwnedStockDB
from ..db.trade import BuyDB, SellDB
from ..models.actions import Buy, BuyInDB, Sell, SellInDB
from ..models.user import User


# TODO add pending trade to user


async def buy_stock(info: Buy) -> User:
    await get_stock(info.stock_id)

    max_funds = info.upper_bound * info.total
    user = await remove_funds(info.user_id, max_funds)

    stock_to_buy = BuyInDB(
        user_id=info.user_id,
        stock_id=info.stock_id,
        total=info.total,
        upper_bound=info.upper_bound,
        lower_bound=info.lower_bound,
        funds=max_funds
    )
    await BuyDB.insert(stock_to_buy.dict())

    return user


async def sell_stock(info: Sell) -> User:
    await get_stock(info.stock_id)

    user = await get_user(info.user_id)
    owned_stock = [s for s in user.stock if s.stock_id == info.stock_id]

    if not owned_stock:
        raise HTTPException(404, "Stock Not Owned By User")

    owned_stock = owned_stock[0]

    if info.total > owned_stock.total:
        raise HTTPException(400, "Not Enough Stock")

    stock_to_sell = SellInDB(**owned_stock.dict(), total=info.total)
    owned_stock.total -= info.total

    await OwnedStockDB.update(
        {"total": owned_stock.total},
        user_id=info.user_id
    )

    await SellDB.insert(stock_to_sell.dict())

    return user
