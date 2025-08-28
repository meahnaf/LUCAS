

import logging
from modules.db.database import execute_query
from utils.utils import generate_md5_hash


def is_new_file_content(path, uploaded_file):
    """Check if the file content is new or already exists in the database.

    Args:
        uploaded_file: The uploaded file.

    Returns:
        True if the file content is new, False otherwise.
    """
    try:
        content_hash = generate_md5_hash(uploaded_file)
        return not check_if_file_hash_exists(path, uploaded_file.name, content_hash)
    except Exception as e:
        raise

def check_if_file_hash_exists(path, file_name, content_hash):
    """Check if the file hash exists in the database.

    Args:
        path: The path of the file.
        file_name: The name of the file.
        content_hash: The hash of the file content.

    Returns:
        True if the hash exists, False otherwise.
    """
    # Check if the hash exists in the database
    # table in postgres called file_metadata with columns path, file_name, content_hash
    # Example usage
    query = """
        SELECT path, name, contenthash
        FROM public.file_metadata
        WHERE path = %s AND name = %s AND contenthash = %s;
        """
    params = (path, file_name, content_hash)
    results = execute_query(query, params)

    if results is None or len(results) == 0:
        return True
    
    return False

def add_or_update_file_metadata(path, file_name, content_hash):
    """
    Add the file metadata to the database also deletes past entries.

    Args:
        path: The path of the file.
        file_name: The name of the file.
        content_hash: The hash of the file content.
    """
    # Add the file metadata to the database
    # table in postgres called file_metadata with columns path, file_name, content_hash
    # Example usage
    try:
        query_delete = """
            DELETE FROM public.file_metadata
            WHERE path = %s AND name = %s;
            """
        query_insert = """
            INSERT INTO public.file_metadata(
            name, path, contenthash)
            VALUES (%s, %s, %s);
            """
        execute_query(query_delete, (path, file_name))
        execute_query(query_insert, (file_name, path, content_hash))  
        #params = (path, file_name, file_name, path, content_hash)
        #execute_query(query, params)
    except Exception as e:
        logging.error(f"Error while adding file metadata: {str(e)}")
        raise

def delete_file_metadata(path, file_name):
    """
    Delete the file metadata from the database.

    Args:
    path: The path of the file.
    file_name: The name of the file.
    """
    try:
        query = """
        DELETE FROM public.file_metadata
        WHERE path = %s AND name = %s;
        """
        params = (path, file_name)
        execute_query(query, params)
    except Exception as e:
        logging.error(f"Error while deleting file metadata: {str(e)}")
        raise