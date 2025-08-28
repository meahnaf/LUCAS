import hashlib

def generate_md5_hash(uploaded_file):
    """Generate MD5 hash of the file contents using a buffer.

    Args:
        uploaded_file: The uploaded file.

    Returns:
        content_hash: MD5 hash of the file contents"""
    hash_md5 = hashlib.md5()
    uploaded_file.seek(0)  # Reset the file pointer to the beginning before reading
    for chunk in iter(lambda: uploaded_file.read(4096), b""):
        hash_md5.update(chunk)
    content_hash = hash_md5.hexdigest()
    uploaded_file.seek(0)  # Reset the file pointer to the beginning after reading
    return content_hash