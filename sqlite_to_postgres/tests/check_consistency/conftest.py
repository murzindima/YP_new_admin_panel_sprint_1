import os
from typing import Dict

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def settings() -> Dict[str, str]:
    """
    Provide a dictionary containing database configuration settings.

    This fixture retrieves SQLite and PostgreSQL database configuration settings from
    environment variables and returns them in a dictionary format. It is designed to
    ensure the required environment variables are set before the tests are executed.

    The required environment variables are:
    - SQLITE_DB_PATH: Path to the SQLite database.
    - POSTGRES_HOST: PostgreSQL host address.
    - POSTGRES_DBNAME: PostgreSQL database name.
    - POSTGRES_USER: PostgreSQL user.
    - POSTGRES_PASSWORD: PostgreSQL password.

    Returns:
    - dict: A dictionary with keys being the setting names and values being the respective
            environment variable values. It also includes a predefined list of table names
            under the "TABLES" key.

    Raises:
    - ValueError: If any of the required environment variables are not set.

    Note:
    The 'tables' list is hard-coded and may need to be updated if the database schema changes.
    """
    db_path = os.getenv("SQLITE_DB_PATH")
    if not db_path:
        raise ValueError("SQLITE_DB_PATH environment variable not set")

    host = os.getenv("POSTGRES_HOST")
    dbname = os.getenv("POSTGRES_DBNAME")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    if not all([host, dbname, user, password]):
        raise ValueError("One or more PostgreSQL environment variables are not set")

    tables = ["genre", "film_work", "person", "genre_film_work", "person_film_work"]

    return {
        "SQLITE_DB_PATH": db_path,
        "POSTGRES_HOST": host,
        "POSTGRES_DBNAME": dbname,
        "POSTGRES_USER": user,
        "POSTGRES_PASSWORD": password,
        "TABLES": tables,
    }
