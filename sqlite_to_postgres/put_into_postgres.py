from contextlib import contextmanager
from dataclasses import fields
from typing import Type, List

import psycopg2


@contextmanager
def postgres_conn_context(host: str, dbname: str, user: str, password: str):
    conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
    try:
        yield conn
    finally:
        conn.close()


def insert_into_postgres(
    conn, table_name: str, table_model: Type, records: List[tuple]
):
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
