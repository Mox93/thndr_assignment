from typing import Tuple

from asyncpg import Pool, create_pool


class Order:
    def __init__(self, columns: Tuple[str], asc: bool):
        self.asc = asc
        self.columns = columns

    @classmethod
    def asc(cls, *columns: str) -> "Order":
        return cls(columns, True)

    @classmethod
    def desc(cls, *columns: str) -> "Order":
        return cls(columns, False)

    def query(self) -> str:
        type_ = "ASC" if self.asc else "DESC"
        columns = ", ".join(self.columns)

        return f"ORDER BY {columns} {type_}"


class BaseDB:
    __pool__: Pool
    __table_name__: str

    @classmethod
    async def connect(cls, dsn):
        cls.__pool__ = await create_pool(dsn)

        for table in cls.__subclasses__():
            await table.create()

    @classmethod
    async def disconnect(cls):
        if cls.__pool__:
            await cls.__pool__.close()

    @classmethod
    async def create(cls):
        raise NotImplementedError()

    @classmethod
    async def fetch(cls, *, __order__: Order = None, **kwargs):
        query = f"SELECT * FROM \"{cls.__table_name__}\" "

        keys, values = list(zip(*kwargs.items()))

        conditions = " AND ".join(f"\"{key}\" = ${i}" for i, key in enumerate(keys, 1))
        query += f" WHERE {conditions}"

        if __order__:
            query += __order__.query()

        async with cls.__pool__.acquire() as conn:
            return await conn.fetchrow(query, *values)
