import os
import streamlit as st
import logging
from config.tenant_site_mapping import tenant_site_mapping
from modules.adls import list_subdirectories, list_files_in_directory, download_files_as_zip, delete_files, upload_file
from modules.constant import default_tenant_name
from modules.db.filemanagement.filecontents import delete_file_contents
from modules.db.filemanagement.filemetadata import add_or_update_file_metadata, check_if_file_hash_exists, delete_file_metadata
from modules.ragPreProcess import process_RAG_pipeline
from modules.tenantutlis import get_site_name_by_id
from utils.utils import generate_md5_hash

def display_files_with_checkboxes(files):
    selected_files = []
    if files:
        for index, file_info in enumerate(files):
            size_in_kb = file_info['size'] / 1024
            size_str = f"{size_in_kb:.2f} KB" if size_in_kb < 1024 else f"{size_in_kb / 1024:.2f} MB"
            last_modified_date = file_info['last_modified'].strftime("%Y-%m-%d %H:%M:%S")
            label = f"{file_info['name']} - {size_str}, Uploaded on: {last_modified_date}"
            if st.checkbox(label, key=f"{file_info['name']}_{index}"):
                selected_files.append(file_info['name'])
    return selected_files

def display_directory_page(selected_site_id):
    """Displays directory control panel.

    Args:
        selected_site_id (string): The selected site ID.
    """
    
    selected_site_name = get_site_name_by_id(selected_site_id)
    # Dynamically load logo based on the selected site name
    logo_path = f'logos/{selected_site_id}.png'  # Ensure filenames match site names

    if os.path.exists(logo_path):
        st.image(logo_path, width=200)
    else:
        st.title("LUCAS")
    
    logging.info("Directory Control page")

    root_dir_path = f"{default_tenant_name}/{selected_site_id}"

    st.subheader(f"Upload a File to '{selected_site_name}'")
    logging.info("upload file display.")
    uploaded_files = st.file_uploader("Choose a file to upload", accept_multiple_files=True, key=f"file_uploader")

    if uploaded_files is not None:
        logging.info("upload file is not none.")
        if st.button("Upload File"):
            try:
                for uploaded_file in uploaded_files:
                    process_upload_file(uploaded_file, root_dir_path, selected_site_id)
            except Exception as e:
                logging.error(f"Error while uploading file '{uploaded_file.name}': {str(e)}")
                st.error("Something went wrong while uploading the file.")

    st.subheader(f"Files in '{selected_site_id}'")

    try:
        files = list_files_in_directory(root_dir_path)
        if not files:
            st.warning(f"No files found in {selected_site_id}.")
        else:
            selected_files = display_files_with_checkboxes(files)

            if selected_files:
                col1, col2 = st.columns(2)

                with col1:
                    try:
                        zip_buffer = download_files_as_zip(selected_files, root_dir_path)
                        if zip_buffer:
                            st.download_button(
                                label="Click here to download selected files as ZIP",
                                data=zip_buffer,
                                file_name=f"{default_tenant_name}_chatbot.zip",
                                mime="application/zip"
                            )
                    except Exception as e:
                        logging.error(f"Error while downloading files as ZIP: {str(e)}")
                        st.error("Something went wrong while downloading the files.")

                with col2:
                    if st.button("Delete Selected Files"):
                        try:
                            delete_files(selected_files, root_dir_path)
                            for file_name in selected_files:
                                delete_file_metadata(root_dir_path, file_name)
                                delete_file_contents(root_dir_path, file_name)
                            st.success(f"Selected files deleted from '{selected_site_id}'.")
                            st.rerun()
                        except Exception as e:
                            logging.error(f"Error while deleting files: {str(e)}")
                            st.error("Something went wrong while deleting the files.")
            else:
                st.info("Please select files to download or delete.")
    except Exception as e:
        logging.error(f"Error while listing files in '{selected_site_id}': {str(e)}")
        st.error("Something went wrong while retrieving the files.")
        
def process_upload_file(uploaded_file, root_dir_path, selected_site_id):
    """processes upload file operation for the uploaded file.

    Args:
        uploaded_file (File): The uploaded file.
        root_dir_path (string): The root directory path.
        selected_site_id (string): The selected site ID.
    """
    try:
        content_hash = generate_md5_hash(uploaded_file)
        if check_if_file_hash_exists(root_dir_path, uploaded_file.name, content_hash):
            logging.info(f"Uploading file {uploaded_file.name} to {selected_site_id}")
            # register metadata of the file & upload the file
            add_or_update_file_metadata(root_dir_path, uploaded_file.name, content_hash)
            logging.info(f"File metadata added for '{uploaded_file.name}'")
            
            upload_file(uploaded_file, root_dir_path, selected_site_id)
            logging.info(f"File '{uploaded_file.name}' uploaded successfully.")
            
            # process rag pipeline
            logging.info(f"Processing RAG pipeline for file '{uploaded_file.name}'")
            process_RAG_pipeline(uploaded_file, root_dir_path, content_hash, selected_site_id, default_tenant_name)
            logging.info("procesing rag pre pipeline is completed.")
        else:
            logging.info("duplicate request for same hash.")
        st.toast(f"File '{uploaded_file.name}' uploaded successfully.", icon='🎉')
    except Exception as e:
        file_name = uploaded_file.name if uploaded_file else 'Unknown_file_name'
        logging.error(f"Error while uploading file '{file_name}': {str(e)}")
        st.toast(f"Something went wrong while uploading the file '{file_name}'.", icon='❗️')