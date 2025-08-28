import os
from app.modules.cohere import rerank_documents
from langchain_openai import AzureOpenAIEmbeddings
from langchain_postgres import PGVector
import logging
from app.modules.openai import openai_chat_completions

username = 'ragsystem'
password = 'kuberrag'
host = 'kuberviz-db.postgres.database.azure.com'
port = '5432'
dbname = 'chat_test'
connection_string = f'postgresql+psycopg://{username}:{password}@{host}:{port}/{dbname}'
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint="https://kubertest.openai.azure.com/",
    deployment="openai-embeddings",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    chunk_size=2048
)

# Create a vector store
vector_store_cache = {}

def get_vector_store(collection_name):
    """Get vector store connection, using cache if available.
    Args:
        collection_name: name of the collection.
    Returns:
        A vector store instance.
    """
    if collection_name in vector_store_cache:
        return vector_store_cache[collection_name]
    vector_store = PGVector(
        connection=connection_string,
        embeddings=embeddings,
        collection_name = collection_name
    )
    vector_store_cache[collection_name] = vector_store
    return vector_store

def retrive_rag_info(query, selected_site_id, tenant_id):
    """Retrieve information from the RAG model.
    
    Args:
        query: The query text.
        selected_site_id: The id which a user has access to upload and query.
        tenant_id: ID of the tenant.
    Returns:
        The message response from the RAG model.
    """
    Collection_name = tenant_id + "_" + selected_site_id
    logging.info(Collection_name)
    vector_store = get_vector_store(Collection_name)
    similar = vector_store.similarity_search_with_score(query, k=30)
    if similar is None or len(similar) == 0:
        logging.info("No context found in docs, returning response from gpt.")
        openai_chat_response = openai_chat_completions("No context found", Collection_name, query)
        return openai_chat_response
    documents = [doc[0].page_content for doc in similar]
    scores = [doc[1] for doc in similar]
    file_names = [doc[0].metadata.get('file_name', 'Unknown') for doc in similar if hasattr(doc[0], 'metadata')]
    # Rerank the documents based on the query
    rerank_response = rerank_documents(query, documents)
    document_indices = [result.index for result in rerank_response.results]
    # Separating documents based on the indices from the rerank response
    separated_documents = [documents[index] for index in document_indices]
    separated_file_names = [file_names[index] for index in document_indices]

    # Combine documents and their corresponding file names
    context_with_file_names = "\n".join(f"File: {file_name}\nContent: {document}" for file_name, document in zip(separated_file_names, separated_documents))
    response =  openai_chat_completions(context_with_file_names, Collection_name, query)
    return response
