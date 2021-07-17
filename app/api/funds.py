from fastapi import APIRouter

from ..models.actions import Deposit, Withdraw
from ..models.user import User
from ..utils.funds import add_funds, remove_funds


router = APIRouter(tags=["Funds"])


@router.post("/deposit", response_model=User)
async def deposit(info: Deposit) -> User:
    return await add_funds(info.user_id, info.amount)


@router.post("/withdraw", response_model=User)
async def withdraw(info: Withdraw) -> User:
    return await remove_funds(info.user_id, info.amount)
