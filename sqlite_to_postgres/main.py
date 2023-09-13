import os

from dotenv import load_dotenv

from get_from_sqlite import sqlite_conn_context
from migrate_data import migrate_table
from models import FilmWork, Genre, Person, GenreFilmWork, PersonFilmWork
from put_into_postgres import postgres_conn_context

load_dotenv()


def main():
    db_path = os.getenv("SQLITE_DB_PATH")
    if not db_path:
        raise ValueError("SQLITE_DB_PATH environment variable not set")

    host = os.getenv("POSTGRES_HOST")
    dbname = os.getenv("POSTGRES_DBNAME")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    if not all([host, dbname, user, password]):
        raise ValueError("One or more PostgreSQL environment variables are not set")

    batch_size = os.getenv("BATCH_SIZE")
    if batch_size:
        try:
            batch_size = int(batch_size)
        except ValueError:
            raise ValueError(
                f"Expected BATCH_SIZE to be an integer but got {batch_size}"
            )
    else:
        raise ValueError("BATCH_SIZE environment variable not set")

    with sqlite_conn_context(db_path) as sqlite_conn, postgres_conn_context(
        host, dbname, user, password
    ) as postgres_conn:
        tables = {
            "film_work": FilmWork,
            "genre": Genre,
            "person": Person,
            "genre_film_work": GenreFilmWork,
            "person_film_work": PersonFilmWork,
        }

        for table_name, table_model in tables.items():
            migrate_table(
                sqlite_conn, postgres_conn, table_name, table_model, batch_size
            )


if __name__ == "__main__":
    main()
