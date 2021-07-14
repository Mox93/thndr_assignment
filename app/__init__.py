from fastapi import FastAPI

from .models import (
    Buy,
    Deposit,
    Sell,
    Stock,
    StockRequest,
    User,
    UserRequest,
    Withdraw,
)


app = FastAPI()


@app.post("/deposit", tags=["Balance"])
def deposit(info: Deposit):
    pass


@app.post("/withdraw", tags=["Balance"])
def withdraw(info: Withdraw):
    pass


@app.post("/buy", tags=["Stock"])
def buy(info: Buy):
    pass


@app.post("/sell", tags=["Stock"])
def sell(info: Sell):
    pass


@app.post("/stock", response_model=Stock, tags=["Info"])
def stock(info: StockRequest) -> Stock:
    pass


@app.post("/user", response_model=User, tags=["Info"])
def user(info: UserRequest) -> User:
    pass
