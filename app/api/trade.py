from fastapi import APIRouter

from ..models.actions import BuyCreate, SellCreate
from ..models.user import User
from ..utils.trade import buy_stock, sell_stock


router = APIRouter(tags=["Trade"])


@router.post("/buy", response_model=User)
async def buy(info: BuyCreate) -> User:
    return await buy_stock(info)


@router.post("/sell", response_model=User)
async def sell(info: SellCreate) -> User:
    return await sell_stock(info)
