from . import BaseDB


class UserDB(BaseDB):
    __table_name__ = "users"

    @classmethod
    async def create(cls):
        async with cls.__pool__.acquire() as conn:
            await conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {cls.__table_name__}(
                id uuid PRIMARY KEY,
                name varchar(256),
                balance double precision
            );
            """)
