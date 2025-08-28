from psycopg import sql

import psycopg_pool
import os

# Database connection details
username = 'ragsystem'
password = 'kuberrag'
host = 'kuberviz-db.postgres.database.azure.com'
port = '5432'
dbname = 'chat_test'
connection_string = f'postgresql://{username}:{password}@{host}:{port}/{dbname}'

# Create a connection pool
pool = psycopg_pool.ConnectionPool(connection_string, min_size=1, max_size=10)

def execute_query(query, params=None):
    """executes a query and returns the result.

    Args:
        query (_type_): raw query string.
        params (_type_, optional): query parameters. Defaults to None.

    Returns: 
        result of the query.
    """
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if query.strip().lower().startswith("select"):
                return cur.fetchall()
            else:
                conn.commit()
                return cur.rowcount
