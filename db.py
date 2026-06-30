import aiosqlite

DB = "giveaway.db"

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS entries(
            user_id INTEGER PRIMARY KEY,
            username TEXT
        )
        """)
        await db.commit()

async def add_entry(user_id, username):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT OR IGNORE INTO entries VALUES (?, ?)",
            (user_id, username)
        )
        await db.commit()

async def count_entries():
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT COUNT(*) FROM entries") as cursor:
            row = await cursor.fetchone()
            return row[0]

async def all_entries():
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT user_id, username FROM entries") as cursor:
            return await cursor.fetchall()

async def reset_entries():
    async with aiosqlite.connect(DB) as db:
        await db.execute("DELETE FROM entries")
        await db.commit()
