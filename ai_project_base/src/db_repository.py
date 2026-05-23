import psycopg
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

pool = ConnectionPool(DATABASE_URL)

def log_extraction(input_text: str, email: str | None) -> None:
    with pool.connection() as conn:
        conn.execute(
            "INSERT INTO extraction_log (input_text, email) VALUES (%s, %s)",
            (input_text, email)
        )

def get_history (limit: int = 10) -> list[dict]:
    with pool.connection() as conn:
        results = conn.execute(
            "SELECT id, input_text, email, created_at FROM extraction_log ORDER BY created_at DESC LIMIT %s",
            (limit,),
        ).fetchall()
    return [
        {"id": r[0], "input_text": r[1], "email": r[2], "created_at": r[3]}
        for r in results
    ]