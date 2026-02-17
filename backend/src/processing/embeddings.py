"""
This page acts like a utility code, which converts the text(document or query) 
into embeddings when another part of the system calls for it
"""
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name = "BAAI/bge-base-en-v1.5")

def embed_documents(chunks):
    """
    Create embeddings for the given document
    """
    return embedding_model.embed_documents([chunk.page_content for chunk in chunks])

def embed_query(query: str):
    """
    Create embeddings for query
    """
    return embedding_model.embed_query(query)


