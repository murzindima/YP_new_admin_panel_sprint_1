from typing import Type

from get_from_sqlite import fetch_sqlite_columns, fetch_from_sqlite
from put_into_postgres import insert_into_postgres


def migrate_table(
    sqlite_conn, postgres_conn, table_name: str, table_model: Type, batch_size: int
):
    """
    Migrate data from a table in an SQLite database to a table in a PostgreSQL database.

    This function fetches data in batches from the SQLite table and inserts it into the
    corresponding PostgreSQL table. The migration is performed in a way that avoids
    excessive memory usage, which is particularly useful when dealing with large tables.

    Parameters:
    - sqlite_conn (sqlite3.Connection): SQLite database connection object.
    - postgres_conn (psycopg2.extensions.connection): PostgreSQL database connection object.
    - table_name (str): Name of the table to migrate.
    - table_model (Type): DataClass type representing the table's schema in the PostgreSQL database.
    - batch_size (int): Number of records to fetch and insert in each batch.

    Notes:
    If a record with the same ID already exists in the PostgreSQL table, the insertion
    will be skipped for that record (due to the ON CONFLICT clause in `insert_into_postgres` function).
    """
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
