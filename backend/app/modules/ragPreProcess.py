import psycopg
import tempfile
import logging
import os
from datetime import datetime
from llama_parse import LlamaParse
from langchain.text_splitter import TokenTextSplitter
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from langchain.schema import Document
from langchain_community.embeddings import AzureOpenAIEmbeddings
from llama_parse import LlamaParse
from langchain_postgres import PGVector
import hashlib

from utils.utils import generate_md5_hash

#TODO: Change this to read from config.
username = 'ragsystem'
password = 'kuberrag'
host = 'kuberviz-db.postgres.database.azure.com'
port = '5432'
dbname = 'chat_test'
connection_string = f'postgresql+psycopg://{username}:{password}@{host}:{port}/{dbname}'

#TODO: read from keyvault / env files.
os.environ["OPENAI_API_KEY"] = "4ba1b36ccc504ab1b6e86a2e5898f10c"

def process_RAG_pipeline(uploaded_file, uploaded_file_path, content_hash, selected_site_id, tenant_id):
    """Process the RAG pipeline.

    Args:
        uploaded_file: The uploaded file.
        selected_site_id: The id which a user has access to upload and query.
        uploaded_file_path: path to the file in file storage.
        content_hash: The hash of the file content.
        selected_site_id: The id which a user has access to upload and query.
        tenant_id: ID of the tenant.
    Returns: None
    """
    logging.info("RAG pipeline is been started")

    with tempfile.TemporaryDirectory() as temp_dir:
        documents = []

        # Save the uploaded file to the temporary directory
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Load PDF using LlamaParse
        document = LlamaParse(result_type='markdown').load_data(file_path)
        if document is None:
            logging.info("document is empty")
        else:
            for i in range(len(document)):
                logging.info("text is been added to documents var" + document[i].text)
                documents.append(document[i].text)
        logging.info("document is been parsed")

    
        text_splitter = SentenceTransformersTokenTextSplitter(chunk_size=512, chunk_overlap=72)

        # Split the text content of the documents
        chunks = []
        for doc in documents:
            chunks.extend(text_splitter.split_text(doc))
        logging.info("Documents have been processed and stored in session state.")

        # Create Document objects from the chunks with metadata
        documents_chunked = [Document(page_content=chunk, metadata={"file_name": uploaded_file.name, "file_path": uploaded_file_path, "content_hash": content_hash}) for chunk in chunks]
        logging.info("chunking is been done")

        # Establish the connection
        dbconn = psycopg.connect(
            host=host,
            user=username,
            password=password,
            port=port,
            dbname=dbname,
            connect_timeout=240
        )
        dbconn.autocommit = True
        cur = dbconn.cursor()

        embeddings = AzureOpenAIEmbeddings(
            azure_endpoint="https://kubertest.openai.azure.com/",
            deployment="openai-embeddings",
            openai_api_key=os.environ["OPENAI_API_KEY"],
            chunk_size=2048
        )
        Collection_name = tenant_id + "_" + selected_site_id

        # Create a vector store
        vector_store = PGVector(
            connection=connection_string,
            embeddings=embeddings,
            collection_name=Collection_name,
            use_jsonb=True,
            async_mode=False,
        )

        logging.info("vector store is configured")

        # Insert data into the vector store
        if documents_chunked is not None:
            vector_store.add_documents(documents_chunked)
        
        logging.info("document info is been added to db")

