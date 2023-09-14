from sqlite_to_postgres.get_from_sqlite import sqlite_conn_context
from sqlite_to_postgres.put_into_postgres import postgres_conn_context


def test_data_integrity_between_dbs(settings):
    """
    Test the data integrity between SQLite and PostgreSQL databases by comparing record counts.

    This function iterates over each table name provided in the settings. For each table,
    it retrieves the total count of records from both the SQLite and PostgreSQL databases.
    It then asserts that the record counts in both databases are identical for each table.

    Parameters:
    - settings (dict): A dictionary containing configuration settings. Expected keys include:
        - SQLITE_DB_PATH: Path to the SQLite database.
        - POSTGRES_HOST: PostgreSQL host address.
        - POSTGRES_DBNAME: PostgreSQL database name.
        - POSTGRES_USER: PostgreSQL user.
        - POSTGRES_PASSWORD: PostgreSQL password.
        - TABLES: List of table names to be tested.

    Raises:
    - AssertionError: If the record counts in SQLite and PostgreSQL do not match for a table.

    Note:
    This function provides a high-level integrity check. For detailed record comparison,
    consider using the `test_record_content` function.
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
            sqlite_cursor = sqlite_conn.cursor()
            sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            sqlite_count = sqlite_cursor.fetchone()[0]

            postgres_cursor = postgres_conn.cursor()
            postgres_cursor.execute(f"SELECT COUNT(*) FROM content.{table}")
            postgres_count = postgres_cursor.fetchone()[0]

            assert (
                sqlite_count == postgres_count
            ), f"Record count mismatch in table {table}"
