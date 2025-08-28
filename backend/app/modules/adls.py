import os
import io
import logging
import zipfile
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv
from fastapi import UploadFile
from .constant import default_tenant_name

# Load environment variables
load_dotenv()


# Load environment variables
client_id = os.getenv('AZURE_ADLS_CLIENT_ID')
tenant_id = os.getenv('AZURE_ADLS_TENANT_ID')
client_secret = os.getenv('AZURE_ADLS_CLIENT_SECRET')
account_url = os.getenv('AZURE_ADLS_STORAGE_URL')

container_name = "ragdocs"
parent_directory = default_tenant_name

# Azure credentials setup
credentials = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)

# Initialize DataLakeServiceClient
service_client = DataLakeServiceClient(account_url=account_url, credential=credentials)
file_system_client = service_client.get_file_system_client(file_system=container_name)

def list_subdirectories(parent_directory=default_tenant_name):
    try:
        subdirectories = []
        paths = file_system_client.get_paths(path=parent_directory)
        for path in paths:
            if path.is_directory:
                subdirectories.append(path.name.replace(f"{parent_directory}/", ""))
        return subdirectories
    except Exception as e:
        logging.error(f"Error while listing subdirectories: {e}")
        raise 

def list_files_in_directory(directory_name):
    try:
        files = []
        paths = file_system_client.get_paths(path=directory_name)
        print(paths);
        for path in paths:
            if not path.is_directory:
                file_info = {
                    'name': path.name.replace(f"{directory_name}/", ""),
                    'size': path.content_length,
                    'last_modified': path.last_modified
                }
                files.append(file_info)
        return files
    except Exception as e:
        logging.error(f"Error while listing files in '{directory_name}': {e}")
        raise 

def download_files_as_zip(selected_files, directory_name):
    zip_buffer = io.BytesIO()
    try:
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for file_name in selected_files:
                file_client = file_system_client.get_file_client(f"{directory_name}/{file_name}")
                downloaded_data = file_client.download_file().readall()
                zip_file.writestr(file_name, downloaded_data)
    except Exception as e:
        logging.error(f"Error while downloading and zipping files: {e}")
        raise 
    finally:
        zip_buffer.seek(0)
    return zip_buffer

def delete_files(selected_file, directory_name):
    try:
        file_client = file_system_client.get_file_client(f"{default_tenant_name}/{directory_name}/{selected_file}")
        file_client.delete_file()
    except Exception as e:
        logging.error(f"Error while deleting files: {e}")
        raise 

async def upload_file(uploaded_file: UploadFile, directory_name: str, site_id: str):
    try:
        # Read the file content
        file_content = await uploaded_file.read()
        
        # Create a file client and upload the data
        file_client = file_system_client.get_file_client(f"{directory_name}/{uploaded_file.filename}")
        file_client.upload_data(file_content, overwrite=True)
        
        return {"filename": uploaded_file.filename, "status": "uploaded"}
    except Exception as e:
        logging.error(f"Error while uploading file '{uploaded_file.filename}' to '{directory_name}': {e}")
        raise
