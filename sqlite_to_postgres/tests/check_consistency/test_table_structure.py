from sqlite_to_postgres.get_from_sqlite import sqlite_conn_context
from sqlite_to_postgres.put_into_postgres import postgres_conn_context


def test_table_structure(settings):
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
