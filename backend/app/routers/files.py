from fastapi import APIRouter, Body, File, HTTPException, UploadFile
from typing import List
from datetime import datetime
import logging

from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ..modules.constant import default_tenant_name
from ..modules.adls import delete_files, list_files_in_directory, download_files_as_zip, upload_file

router = APIRouter()

@router.get("/directories/{site_id}/files", tags=["directories"], response_model=List[dict])
def get_files_in_directory(site_id: str):
    """
    API endpoint to fetch files in a specific directory.

    Args:
        site_id (str): The ID of the site, mapping to the directory name.

    Returns:
        List[dict]: A list of files with metadata (name, size, last_modified).
    """
    try:
        # Construct the full directory path
        directory_name = f"{default_tenant_name}/{site_id}"  
        files = list_files_in_directory(directory_name)
        return [
            {
                "name": file["name"],
                "size": file["size"],
                "last_modified": file["last_modified"].strftime("%Y-%m-%d %H:%M:%S") if isinstance(file["last_modified"], datetime) else file["last_modified"],
            }
            for file in files
        ]
    except Exception as e:
        logging.error(f"Error fetching files for site ID '{site_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve files.")


class FileRequestBody(BaseModel):
    selected_files: List[str]

@router.post("/directories/{site_id}/download", tags=["directories"])
def download_files(site_id: str, request_body: FileRequestBody):
    """
    API endpoint to download selected files from a directory as a zip file.
    """
    try:
        # Log incoming data
        logging.info(f"Received request to download files for site_id: {site_id}")
        logging.info(f"Selected files: {request_body.selected_files}")

        # Construct the directory path
        directory_name = f"{default_tenant_name}/{site_id}"

        # Call the function to get the zip buffer
        zip_buffer = download_files_as_zip(request_body.selected_files, directory_name)

        # Return the zip file as a streaming response
        return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=files.zip"})
    except Exception as e:
        logging.error(f"Error while downloading files as zip for site ID '{site_id}': {e}")
        raise HTTPException(status_code=500, detail="Failed to download files as zip.")



@router.post("/directories/{site_id}/upload", tags=["directories"])
async def upload_files(site_id: str, uploaded_files: List[UploadFile] = File(...)):
    """
    API endpoint to upload files to a specific directory.
    Args:
        site_id (str): The ID of the site, mapping to the directory name.
        uploaded_files (List[UploadFile]): List of uploaded files.
    Returns:
        dict: Success message
    """
    try:
        directory_name = f"{default_tenant_name}/{site_id}"
        processed_files = []
        
        # Process each uploaded file
        for uploaded_file in uploaded_files:
            if not uploaded_file.filename:  # Add validation for filename
                raise ValueError("File must have a filename")
                
            logging.info(f"Uploading file: {uploaded_file.filename}")  # Better logging
            
            # Save the file and get the result
            result = await upload_file(uploaded_file, directory_name, site_id)
            processed_files.append(result)
            
        return {
            "message": f"{len(processed_files)} files uploaded successfully.",
            "uploaded_files": processed_files
        }
        
    except ValueError as ve:
        logging.error(f"Validation error during file upload: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Error while uploading files: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to upload files")
    

class DeleteRequest(BaseModel):
    selected_files: list[str]
    directory_name: str
    
@router.post("/directories/{site_id}/delete")
async def delete_files_route(site_id: str, delete_request: DeleteRequest):
    
    try:
        delete_files(delete_request.selected_files[0], delete_request.directory_name)
        return {"status": "success", "message": "Files deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete files: {e}")
