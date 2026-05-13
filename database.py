import aiosqlite

DB_NAME = "roulette.db"

async def setup_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS roulettes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            chat_id INTEGER,
            message_id INTEGER
        )
        ''')

        await db.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roulette_id INTEGER,
            user_id INTEGER
        )
        ''')

        await db.commit()
