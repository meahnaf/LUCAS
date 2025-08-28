import logging
from modules.db.database import execute_query


def delete_file_contents(path, file_name):
    """
    Delete the file contents from the database.

    Args:
        path: The path of the file.
        file_name: The name of the file.
    """
    try:
        query = """
            DELETE FROM public.langchain_pg_embedding
            WHERE cmetadata->>'file_path' = %s AND cmetadata->>'file_name' = %s;
            """
        params = (path, file_name)
        logging.info(f"query: {query}")
        logging.info(f"params: {params}")
        execute_query(query, params)
        logging.info(f"Deleted file contents for {file_name} at {path}")
    except Exception as e:
        logging.error(f"Error while deleting file contents: {str(e)}")
        raise
    