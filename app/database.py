import os
import sqlite3
import aiosqlite
from datetime import datetime
from typing import Optional, Dict, Any

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
DB_PATH = DATABASE_URL.replace("sqlite:///", "")

async def create_tables():
    """Create database tables if they don't exist"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS qa_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

class Database:
    """Database operations class"""
    
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
    
    async def save_qa(self, question: str, answer: str) -> int:
        """Save Q&A entry to database"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "INSERT INTO qa_entries (question, answer, timestamp) VALUES (?, ?, ?)",
                (question, answer, datetime.now())
            )
            await db.commit()
            return cursor.lastrowid
    
    async def get_latest_qa(self) -> Optional[Dict[str, Any]]:
        """Get the latest Q&A entry from database"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM qa_entries ORDER BY timestamp DESC LIMIT 1"
            )
            row = await cursor.fetchone()
            
            if row:
                return {
                    "id": row["id"],
                    "question": row["question"],
                    "answer": row["answer"],
                    "timestamp": row["timestamp"]
                }
            return None
    
    async def get_all_qa(self, limit: int = 10) -> list:
        """Get all Q&A entries with limit"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM qa_entries ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            rows = await cursor.fetchall()
            
            return [
                {
                    "id": row["id"],
                    "question": row["question"],
                    "answer": row["answer"],
                    "timestamp": row["timestamp"]
                }
                for row in rows
            ]

async def get_db():
    """Dependency to get database instance"""
    return Database()