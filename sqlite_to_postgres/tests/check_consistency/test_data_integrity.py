from sqlite_to_postgres.get_from_sqlite import sqlite_conn_context
from sqlite_to_postgres.put_into_postgres import postgres_conn_context


def test_data_integrity_between_dbs(settings):
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
            sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            sqlite_count = sqlite_cursor.fetchone()[0]

            postgres_cursor = postgres_conn.cursor()
            postgres_cursor.execute(f"SELECT COUNT(*) FROM content.{table}")
            postgres_count = postgres_cursor.fetchone()[0]

            assert (
                sqlite_count == postgres_count
            ), f"Record count mismatch in table {table}"
