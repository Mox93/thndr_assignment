from uuid import UUID

from fastapi import HTTPException

from .stock import get_owned_stock
from ..db.user import UserDB
from ..models.user import User, UserInDB


async def get_user(user_id: UUID, include_stock: bool = True) -> User:
    user_db = await UserDB.fetch_one(id=user_id)

    if not user_db:
        raise HTTPException(404, "User Not Found")

    user_db = UserInDB.parse_obj(user_db)

    stock = await get_owned_stock(user_id) if include_stock else set()

    return User(
        user_id=user_db.id,
        name=user_db.name,
        balance=user_db.balance,
        stock=stock
    )
