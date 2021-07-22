from fastapi import HTTPException

from .funds import add_funds, remove_funds
from .stock import get_stock
from .user import get_user
from ..db import Le, Ge
from ..db.stock import OwnedStockDB
from ..db.trade import BuyDB, SellDB
from ..db.user import UserDB
from ..models.actions import Buy, BuyInDB, Sell, SellInDB
from ..models.stock import Stock
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

    [owned_stock] = owned_stock

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


async def resolve_buyers(stock: Stock) -> Stock:
    buyers_db = await BuyDB.fetch_many(
        stock_id=stock.stock_id,
        upper_bound=Ge(stock.price),
        lower_bound=Le(stock.price)
    )

    for buyer_db in buyers_db:
        if not stock.availability:
            break

        buyer = BuyInDB.parse_obj(buyer_db)
        user = await get_user(buyer.user_id)
        owned_stock = [s for s in user.stock if s.stock_id == stock.stock_id]
        allocated = min(buyer.total, stock.availability)
        cost = stock.price * allocated

        stock.availability -= allocated
        buyer.total -= allocated
        buyer.funds -= cost

        if owned_stock:
            [owned_stock] = owned_stock

            await OwnedStockDB.update(
                {"total": owned_stock.total + allocated},
                user_id=user.user_id
            )
        else:
            await OwnedStockDB.insert(
                {
                    "user_id": user.user_id,
                    "stock_id": stock.stock_id,
                    "name": stock.name,
                    "total": allocated
                }
            )

        if buyer.total:
            await BuyDB.update(
                {"total": buyer.total, "funds": buyer.funds},
                stock_id=stock.stock_id
            )
        else:
            await UserDB.update(
                {"balance": user.balance + buyer.funds},
                id=user.user_id
            )
            await BuyDB.delete(stock_id=stock.stock_id, user_id=user.user_id)

    return stock


async def resolve_sellers(stock: Stock) -> Stock:
    sellers_db = await SellDB.fetch_many(
        stock_id=stock.stock_id,
        upper_bound=Ge(stock.price),
        lower_bound=Le(stock.price)
    )

    for seller_db in sellers_db:
        seller = SellInDB.parse_obj(seller_db)
        total_price = stock.price * seller.total

        stock.availability += seller.total

        await SellDB.delete(stock_id=stock.stock_id, user_id=seller.user_id)
        await add_funds(seller.user_id, total_price)

        return stock
