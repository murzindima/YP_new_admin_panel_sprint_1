import os
from typing import Dict, Optional

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def settings() -> Dict[str, str]:
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
