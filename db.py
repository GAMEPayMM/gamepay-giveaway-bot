import aiosqlite
from config import DB_NAME


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS entries(
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT
            )
        """)
        await db.commit()


async def add_entry(user):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT user_id FROM entries WHERE user_id=?",
            (user.id,)
        )

        exists = await cursor.fetchone()

        if exists:
            return False

        await db.execute(
            """
            INSERT INTO entries
            (user_id, username, first_name)
            VALUES (?, ?, ?)
            """,
            (
                user.id,
                user.username,
                user.first_name
            )
        )

        await db.commit()

        return True


async def count_entries():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM entries") as cursor:
            row = await cursor.fetchone()
            return row[0]


async def all_entries():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT user_id, username, first_name FROM entries"
        ) as cursor:
            return await cursor.fetchall()


async def reset_entries():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM entries")
        await db.commit()
