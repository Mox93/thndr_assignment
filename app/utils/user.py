from uuid import UUID

from fastapi import HTTPException

from ..db.user import UserDB
from ..models.user import User, UserInDB


async def get_user(user_id: UUID) -> User:
    user_db = await UserDB.fetch(id=user_id)

    if not user_db:
        raise HTTPException(404, "User Not Found")

    user_db = UserInDB.parse_obj(user_db)

    stock = []

    return User(
        user_id=user_db.id,
        name=user_db.name,
        balance=user_db.balance,
        stoke=stock
    )
