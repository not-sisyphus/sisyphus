import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("DATABASE_URL")

async def initialize_database():
    conn = await asyncpg.connect(connection_string)

    try:
        # Create Users table first
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                session_id INTEGER
            );
        """)

        # Create Sessions table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS Sessions (
                id SERIAL PRIMARY KEY,
                creator_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
                code TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

        # Add foreign key to Users table after Sessions exists
        await conn.execute("""
            ALTER TABLE Users 
            ADD CONSTRAINT fk_session 
            FOREIGN KEY (session_id) 
            REFERENCES Sessions(id) 
            ON DELETE SET NULL;
        """)

        # Create Votes table
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS Votes (
                id SERIAL PRIMARY KEY,
                session_id INTEGER NOT NULL REFERENCES Sessions(id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
                value INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)

    finally:
        await conn.close()

# Example usage:
if __name__ == "__main__":
    import asyncio
    asyncio.run(initialize_database())