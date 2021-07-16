from fastapi import APIRouter

from ..models.actions import Buy, Sell


router = APIRouter(tags=["Trade"])


@router.post("/buy")
async def buy(info: Buy):
    pass


@router.post("/sell")
async def sell(info: Sell):
    pass
