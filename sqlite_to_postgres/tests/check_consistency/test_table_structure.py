from sqlite_to_postgres.get_from_sqlite import sqlite_conn_context
from sqlite_to_postgres.put_into_postgres import postgres_conn_context


def test_table_structure(settings):
    """
    Test the table structure consistency between SQLite and PostgreSQL databases.

    This function verifies that the columns present in tables from both SQLite and PostgreSQL
    databases are identical. It iterates over each table name provided in the settings, retrieves
    the column names for each table, and asserts that the column sets are the same for each database.

    Parameters:
    - settings (dict): A dictionary containing configuration settings. Expected keys include:
        - SQLITE_DB_PATH: Path to the SQLite database.
        - POSTGRES_HOST: PostgreSQL host address.
        - POSTGRES_DBNAME: PostgreSQL database name.
        - POSTGRES_USER: PostgreSQL user.
        - POSTGRES_PASSWORD: PostgreSQL password.
        - TABLES: List of table names to be tested.

    Raises:
    - AssertionError: If the column sets in SQLite and PostgreSQL tables do not match.

    Note:
    The 'file_path' column, if present in SQLite tables, is ignored during comparison.
    """
    with sqlite_conn_context(
        settings["SQLITE_DB_PATH"]
    ) as sqlite_conn, postgres_conn_context(
        settings["POSTGRES_HOST"],
        settings["POSTGRES_DBNAME"],
        settings["POSTGRES_USER"],
        settings["POSTGRES_PASSWORD"],
    ) as postgres_conn:
        for table in settings["TABLES"]:
            sqlite_cursor = sqlite_conn.cursor()
            postgres_cursor = postgres_conn.cursor()

            sqlite_cursor.execute(f"PRAGMA table_info({table});")
            sqlite_columns = [column[1] for column in sqlite_cursor.fetchall()]
            if "file_path" in sqlite_columns:
                sqlite_columns.remove("file_path")

            postgres_cursor.execute(
                f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'content' AND table_name = '{table}';
            """
            )
            postgres_columns = [row[0] for row in postgres_cursor.fetchall()]

            assert set(sqlite_columns) == set(
                postgres_columns
            ), f"Structure mismatch in table {table}"
