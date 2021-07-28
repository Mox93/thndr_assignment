from uuid import UUID

from fastapi import HTTPException

from .user import get_user
from ..db.user import UserDB
from ..models.user import User, UserInDB


async def add_funds(user_id: UUID, amount: float) -> User:
    user = await get_user(user_id)
    user_db = await UserDB.update(
        {"balance": user.balance + amount},
        id=user_id
    )
    user_db = UserInDB.parse_obj(user_db[0])

    return User(
        user_id=user_db.id,
        name=user_db.name,
        balance=user_db.balance,
        stock=user.stock,
        pending_buys=user.pending_buys,
        pending_sells=user.pending_sells,
    )


async def remove_funds(user_id: UUID, amount: float) -> User:
    user = await get_user(user_id)

    if amount > user.balance:
        raise HTTPException(400, "Not Enough Balance")

    user_db = await UserDB.update(
        {"balance": user.balance - amount},
        id=user_id
    )
    user_db = UserInDB.parse_obj(user_db[0])

    return User(
        user_id=user_db.id,
        name=user_db.name,
        balance=user_db.balance,
        stock=user.stock,
        pending_buys=user.pending_buys,
        pending_sells=user.pending_sells,
    )
