from . import BaseDB
from .stock import StockDB
from .user import UserDB


class BuyDB(BaseDB):
    __table_name__ = "buy"

    @classmethod
    async def create(cls):
        async with cls.__pool__.acquire() as conn:
            await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS "{cls.__table_name__}"(
                user_id uuid REFERENCES "{UserDB.__table_name__}"(id) NOT NULL,
                stock_id uuid REFERENCES {StockDB.__table_name__}(id) NOT NULL,
                upper_bound double precision NOT NULL,
                lower_bound double precision NOT NULL,
                total integer NOT NULL,
                funds double precision NOT NULL
            );
""")


class SellDB(BaseDB):
    __table_name__ = "sell"

    @classmethod
    async def create(cls):
        async with cls.__pool__.acquire() as conn:
            await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS "{cls.__table_name__}"(
                user_id uuid REFERENCES "{UserDB.__table_name__}"(id) NOT NULL,
                stock_id uuid REFERENCES {StockDB.__table_name__}(id) NOT NULL,
                upper_bound double precision NOT NULL,
                lower_bound double precision NOT NULL,
                total integer NOT NULL
            );
""")
