from uuid import UUID

from fastapi import HTTPException

from .stock import get_owned_stock
from ..db.user import UserDB
from ..db.trade import BuyDB, SellDB
from ..models.user import User, UserInDB
from ..models.actions import Buy, Sell


async def get_user(
        user_id: UUID,
        include_stock: bool = True,
        include_pending_trade: bool = True
) -> User:
    user_db = await UserDB.fetch_one(id=user_id)

    if not user_db:
        raise HTTPException(404, "User Not Found")

    user_db = UserInDB.parse_obj(user_db)
    stock = await get_owned_stock(user_id) if include_stock else []
    pending_buys = []
    pending_sells = []

    if include_pending_trade:
        buys_db = await BuyDB.fetch_many(user_id=user_db.id)
        sells_db = await SellDB.fetch_many(user_id=user_db.id)

        pending_buys.extend(Buy.parse_obj(buy_db) for buy_db in buys_db)
        pending_sells.extend(Sell.parse_obj(sell_db) for sell_db in sells_db)

    return User(
        user_id=user_db.id,
        name=user_db.name,
        balance=user_db.balance,
        stock=stock,
        pending_buys=pending_buys,
        pending_sells=pending_sells,
    )
