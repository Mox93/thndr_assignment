from typing import Any, Dict, Tuple

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

        return f" ORDER BY {columns} {type_} "


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
    async def fetch_one(cls, *, __order__: Order = None, **kwargs):
        query = f"SELECT * FROM \"{cls.__table_name__}\" "
        values = []

        if kwargs:
            keys, values = [x for x in zip(*kwargs.items())]
            conditions = " AND ".join(
                f"\"{key}\" = ${i}" for i, key in enumerate(keys, 1)
            )
            query += f" WHERE {conditions} "

        if __order__:
            query += __order__.query()

        async with cls.__pool__.acquire() as conn:
            return await conn.fetchrow(query, *values)

    @classmethod
    async def fetch_many(cls, **kwargs):
        query = f"SELECT * FROM \"{cls.__table_name__}\" "
        values = []

        if kwargs:
            keys, values = [x for x in zip(*kwargs.items())]
            conditions = " AND ".join(
                f"\"{key}\" = ${i}" for i, key in enumerate(keys, 1)
            )
            query += f" WHERE {conditions} "

        async with cls.__pool__.acquire() as conn:
            return await conn.fetch(query, *values)

    @classmethod
    async def insert(cls, data: Dict[str, Any]):
        keys, values = [x for x in zip(*data.items())]
        query = f"""
        INSERT INTO {cls.__table_name__} ({", ".join(keys)})
        VALUES ({", ".join(f"${i + 1}" for i in range(len(values)))})
"""

        async with cls.__pool__.acquire() as conn:
            return await conn.fetch(query, *values)

    @classmethod
    async def update(cls, updates: Dict[str, Any], **kwargs):
        keys, values = [x for x in zip(*updates.items())]
        changes = ", ".join(
            f"\"{key}\" = ${i}" for i, key in enumerate(keys, 1)
        )
        query = f"UPDATE \"{cls.__table_name__}\" SET {changes} "

        if kwargs:
            keys, values_ = [x for x in zip(*kwargs.items())]
            conditions = " AND ".join(
                f"\"{key}\" = ${i}" for i, key in enumerate(keys, len(values) + 1)
            )
            query += f" WHERE {conditions} "
            values += values_

        query += f"RETURNING *;"

        async with cls.__pool__.acquire() as conn:
            return await conn.fetch(query, *values)
