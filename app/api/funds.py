from fastapi import APIRouter

from ..models.actions import Deposit, Withdraw


router = APIRouter(tags=["Funds"])


@router.post("/deposit")
async def deposit(info: Deposit):
    pass


@router.post("/withdraw")
async def withdraw(info: Withdraw):
    pass
