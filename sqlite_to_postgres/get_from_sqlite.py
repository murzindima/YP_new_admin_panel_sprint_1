import logging
import sqlite3
from contextlib import contextmanager
from typing import List

EXCLUDED_COLUMN = "file_path"
logger = logging.getLogger(__name__)


@contextmanager
def sqlite_conn_context(db_path: str):
    """
    Context manager for managing SQLite database connections.

    This context manager provides a connection to the SQLite database and ensures
    the connection is properly closed after usage.

    Parameters:
    - db_path (str): Path to the SQLite database file.

    Yields:
    - sqlite3.Connection: SQLite database connection object.

    Example:
    with sqlite_conn_context('path/to/db.sqlite3') as conn:
        # Perform database operations using conn
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def fetch_sqlite_columns(conn, table_name: str) -> List[str]:
    """
    Fetch the column names of a given table in the SQLite database.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection object.
    - table_name (str): Name of the table to fetch columns for.

    Returns:
    - List[str]: List of column names for the given table.

    Raises:
    - sqlite3.Error: If there's an error in querying the SQLite database.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        return columns
    except sqlite3.Error as e:
        logger.exception(f"SQLite error occurred while fetching columns: {e}")
        return []


def fetch_from_sqlite(
    conn, table_name: str, columns: List[str], offset: int, batch_size: int
) -> List[tuple]:
    """
    Fetch a batch of rows from a table in the SQLite database based on the provided offset and batch size.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection object.
    - table_name (str): Name of the table to fetch rows from.
    - columns (List[str]): List of column names to fetch.
    - offset (int): Starting point for fetching rows.
    - batch_size (int): Number of rows to fetch.

    Returns:
    - List[tuple]: List of rows fetched from the table. Each row is represented as a tuple.

    Raises:
    - sqlite3.Error: If there's an error in querying the SQLite database.
    """
    try:
        cursor = conn.cursor()
        if EXCLUDED_COLUMN in columns:
            columns.remove(EXCLUDED_COLUMN)
        cursor.execute(
            f"SELECT {','.join(columns)} FROM {table_name} LIMIT {batch_size} OFFSET {offset}"
        )
        return cursor.fetchall()
    except sqlite3.Error as e:
        logger.exception(f"SQLite error occurred while fetching data: {e}")
        return []
