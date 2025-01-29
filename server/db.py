# init_db.py
import sqlite3

database_path = "database.sqlite"


def initialize_database():
	conn = sqlite3.connect(database_path)
	try:
		cursor = conn.cursor()

		# Create Users table first
		cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                session_id INTEGER,
                FOREIGN KEY (session_id) REFERENCES Sessions(id) ON DELETE SET NULL
            );
        """)

		# Create Sessions table
		cursor.execute("""
            CREATE TABLE IF NOT EXISTS Sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES Users(id) ON DELETE CASCADE
            );
        """)

		# Create Votes table
		cursor.execute("""
            CREATE TABLE IF NOT EXISTS Votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                value INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES Sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
            );
        """)

		conn.commit()
	finally:
		conn.close()


if __name__ == "__main__":
	initialize_database()