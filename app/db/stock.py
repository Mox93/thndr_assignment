from . import BaseDB
from .user import UserDB


class StockDB(BaseDB):
    __table_name__ = "stock"

    @classmethod
    async def create(cls):
        async with cls.__pool__.acquire() as conn:
            await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {cls.__table_name__}(
                id uuid PRIMARY KEY,
                name varchar(256) NOT NULL
            );
""")


class StockStreamDB(BaseDB):
    __table_name__ = "stock_stream"

    @classmethod
    async def create(cls):
        async with cls.__pool__.acquire() as conn:
            await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {cls.__table_name__}(
                stock_id uuid REFERENCES {StockDB.__table_name__}(id)  NOT NULL,
                timestamp timestamp NOT NULL,
                price real NOT NULL,
                availability integer NOT NULL
            );
""")


class OwnedStockDB(BaseDB):
    __table_name__ = "owned_stock"

    @classmethod
    async def create(cls):
        async with cls.__pool__.acquire() as conn:
            await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {cls.__table_name__}(
                user_id uuid REFERENCES "{UserDB.__table_name__}"(id) NOT NULL,
                stock_id uuid REFERENCES {StockDB.__table_name__}(id) NOT NULL,
                name varchar(256) NOT NULL,
                total integer NOT NULL,
                UNIQUE(user_id, stock_id)
            );
""")
