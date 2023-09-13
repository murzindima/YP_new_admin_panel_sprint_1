from typing import Type

from get_from_sqlite import fetch_sqlite_columns, fetch_from_sqlite
from put_into_postgres import insert_into_postgres


def migrate_table(
    sqlite_conn, postgres_conn, table_name: str, table_model: Type, batch_size: int
):
    columns = fetch_sqlite_columns(sqlite_conn, table_name)
    offset = 0

    while True:
        records = fetch_from_sqlite(
            sqlite_conn, table_name, columns, offset, batch_size
        )

        if not records:
            break

        insert_into_postgres(postgres_conn, table_name, table_model, records)

        offset += batch_size
