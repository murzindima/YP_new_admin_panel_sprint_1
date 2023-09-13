import sqlite3
from contextlib import contextmanager
from typing import List

EXCLUDED_COLUMN = "file_path"


@contextmanager
def sqlite_conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def fetch_sqlite_columns(conn, table_name: str) -> List[str]:
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        return columns
    except sqlite3.Error as e:
        print(f"SQLite error occurred while fetching columns: {e}")
        return []


def fetch_from_sqlite(
    conn, table_name: str, columns: List[str], offset: int, batch_size: int
) -> List[tuple]:
    try:
        cursor = conn.cursor()
        if EXCLUDED_COLUMN in columns:
            columns.remove(EXCLUDED_COLUMN)
        cursor.execute(
            f"SELECT {','.join(columns)} FROM {table_name} LIMIT {batch_size} OFFSET {offset}"
        )
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"SQLite error occurred while fetching data: {e}")
        return []
