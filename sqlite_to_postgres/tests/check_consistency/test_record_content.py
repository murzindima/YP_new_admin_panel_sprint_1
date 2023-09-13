from datetime import datetime

from sqlite_to_postgres.get_from_sqlite import sqlite_conn_context
from sqlite_to_postgres.put_into_postgres import postgres_conn_context


def test_record_content(settings):
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
            columns = [
                column[1]
                for column in sqlite_cursor.fetchall()
                if column[1] != "file_path"
            ]

            sqlite_cursor.execute(f"SELECT {','.join(columns)} FROM {table}")
            sqlite_records_raw = sqlite_cursor.fetchall()

            sqlite_records = set()
            for record in sqlite_records_raw:
                normalized_record = []
                for item in record:
                    if isinstance(item, str) and "+" in item:
                        normalized_record.append(datetime.fromisoformat(item))
                    else:
                        normalized_record.append(item)
                sqlite_records.add(tuple(normalized_record))

            postgres_cursor.execute(f"SELECT {','.join(columns)} FROM content.{table}")
            postgres_records = set(postgres_cursor.fetchall())

            assert sqlite_records == postgres_records, f"Data mismatch in table {table}"
