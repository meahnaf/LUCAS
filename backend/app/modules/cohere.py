import cohere
# Initialize Cohere client
cohere_client = cohere.Client('y0yIK9X1eVnTU3pkijqpJZKMlpCnENpAmRnQ2fpA')

def rerank_documents(query, documents):
    """Rerank the documents based on the query.
    
    Args:
        query: The query text.
        documents: The list of documents to rerank.
    
    Returns:
        The reranked documents.
    """
    rerank_response = cohere_client.rerank(
        query=query,
        documents=documents,
        top_n=15, model='rerank-english-v3.0'
    )
    return rerank_response
