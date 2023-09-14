import dataclasses
from datetime import datetime
from dateutil.parser import parse

from sqlite_to_postgres.get_from_sqlite import sqlite_conn_context
from sqlite_to_postgres.models import (
    FilmWork,
    Genre,
    Person,
    GenreFilmWork,
    PersonFilmWork,
)
from sqlite_to_postgres.put_into_postgres import postgres_conn_context

TABLE_MODEL_MAPPING = {
    "film_work": FilmWork,
    "genre": Genre,
    "person": Person,
    "genre_film_work": GenreFilmWork,
    "person_film_work": PersonFilmWork,
}


def test_record_content(settings):
    """
    Test the consistency of record content between SQLite and PostgreSQL databases.

    This function fetches records from the SQLite and PostgreSQL databases based on the
    table names provided in the settings. For each table, it retrieves the records and
    normalizes date-time strings to datetime objects for comparison. After normalization,
    it asserts that the records in both databases are identical.

    The function uses dataclass models defined for each table to assist with data normalization.

    Parameters:
    - settings (dict): A dictionary containing configuration settings. Expected keys include:
        - SQLITE_DB_PATH: Path to the SQLite database.
        - POSTGRES_HOST: PostgreSQL host address.
        - POSTGRES_DBNAME: PostgreSQL database name.
        - POSTGRES_USER: PostgreSQL user.
        - POSTGRES_PASSWORD: PostgreSQL password.
        - TABLES: List of table names to be tested.

    Raises:
    - ValueError: If no model is found for a table.
    - AttributeError: If a model does not have an expected attribute.
    - AssertionError: If the records in SQLite and PostgreSQL do not match for a table.

    Note:
    Ensure the dataclass models are correctly defined and in sync with the database schema.
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
            model = TABLE_MODEL_MAPPING.get(table)
            if not model:
                raise ValueError(f"No model found for table {table}")

            sqlite_cursor = sqlite_conn.cursor()
            postgres_cursor = postgres_conn.cursor()

            columns = [field.name for field in dataclasses.fields(model)]

            sqlite_cursor.execute(f"SELECT {','.join(columns)} FROM {table}")
            sqlite_records_raw = sqlite_cursor.fetchall()

            # Get the field names from the dataclass definition
            dataclass_fields = [field.name for field in dataclasses.fields(model)]
            dataclass_field_types = {
                field.name: field.type for field in dataclasses.fields(model)
            }

            sqlite_records = set()
            for record in sqlite_records_raw:
                normalized_record = []
                for idx, column_name in enumerate(columns):
                    # Check if the column_name exists in the dataclass fields
                    if column_name in dataclass_fields:
                        field_type = dataclass_field_types[column_name]
                        item = record[idx]
                        if field_type == datetime and isinstance(item, str):
                            # Convert ISO-formatted string to datetime object
                            item = parse(item)
                        normalized_record.append(item)
                    else:
                        raise AttributeError(
                            f"{model.__name__} has no attribute '{column_name}'"
                        )

                sqlite_records.add(tuple(normalized_record))

            postgres_cursor.execute(f"SELECT {','.join(columns)} FROM content.{table}")
            postgres_records = set(postgres_cursor.fetchall())

            assert sqlite_records == postgres_records, f"Data mismatch in table {table}"
