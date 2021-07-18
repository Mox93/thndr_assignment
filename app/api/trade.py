from fastapi import APIRouter

from ..models.actions import Buy, Sell
from ..models.user import User
from ..utils.trade import buy_stock, sell_stock


router = APIRouter(tags=["Trade"])


@router.post("/buy", response_model=User)
async def buy(info: Buy) -> User:
    return await buy_stock(info)


@router.post("/sell", response_model=User)
async def sell(info: Sell) -> User:
    return await sell_stock(info)
