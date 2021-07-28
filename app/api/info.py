from typing import Union

from fastapi import APIRouter

from ..models.stock import Stock, StockDuration, StockRequest
from ..models.user import User, UserRequest
from ..utils.user import get_user
from ..utils.stock import get_stock


router = APIRouter(tags=["Info"])


@router.post("/stock", response_model=Union[Stock, StockDuration])
async def stock(info: StockRequest) -> Union[Stock, StockDuration]:
    return await get_stock(info)


@router.post("/user", response_model=User)
async def user(info: UserRequest) -> User:
    return await get_user(info.user_id)
