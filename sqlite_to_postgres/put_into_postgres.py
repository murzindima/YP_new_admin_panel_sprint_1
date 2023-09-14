from contextlib import contextmanager
from dataclasses import fields
from typing import Type, List

import psycopg2


@contextmanager
def postgres_conn_context(host: str, dbname: str, user: str, password: str):
    """
    Context manager for managing PostgreSQL database connections.

    This context manager provides a connection to the PostgreSQL database and ensures
    the connection is properly closed after usage.

    Parameters:
    - host (str): Host address of the PostgreSQL database server.
    - dbname (str): Name of the database to connect to.
    - user (str): Username to use for authentication.
    - password (str): Password to use for authentication.

    Yields:
    - psycopg2.extensions.connection: PostgreSQL database connection object.

    Example:
    with postgres_conn_context('localhost', 'mydb', 'user', 'pass') as conn:
        # Perform database operations using conn
    """
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        yield conn
    finally:
        conn.close()


def insert_into_postgres(
    conn, table_name: str, table_model: Type, records: List[tuple]
):
    """
    Insert a batch of records into a table in the PostgreSQL database.

    If a record with the same ID already exists in the table, the insertion will
    be skipped for that record (due to the ON CONFLICT clause).

    Parameters:
    - conn (psycopg2.extensions.connection): PostgreSQL database connection object.
    - table_name (str): Name of the table to insert records into.
    - table_model (Type): DataClass type representing the table's schema.
    - records (List[tuple]): List of records to insert. Each record is represented as a tuple.

    Raises:
    - psycopg2.Error: If there's an error in inserting records into PostgreSQL.
    """
    cursor = conn.cursor()
    schema = "content"
    columns = [f.name for f in fields(table_model)]
    placeholders = ", ".join(["%s"] * len(columns))

    insert_query = f"""
    INSERT INTO {schema}.{table_name} ({','.join(columns)})
    VALUES ({placeholders})
    ON CONFLICT (id) DO NOTHING;
    """

    try:
        for record in records:
            cursor.execute(insert_query, record)
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error inserting record into PostgreSQL: {e}")
        conn.rollback()
