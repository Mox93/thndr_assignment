from fastapi import FastAPI

from .api import funds, trade, info
from .db import BaseDB
from .internal import internal


app = FastAPI()


@app.on_event("startup")
async def startup():
    from .utils.settings import settings

    await BaseDB.connect(settings().pg_dsn)


@app.on_event("shutdown")
async def shutdown():
    await BaseDB.disconnect()


app.include_router(funds.router)
app.include_router(trade.router)
app.include_router(info.router)

app.mount("/internal", internal)
