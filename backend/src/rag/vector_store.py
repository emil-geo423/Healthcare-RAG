import faiss
import numpy as np

from src.processing.embeddings import embed_documents, embed_query
from src.processing.chunking import chunk_documents
from src.loaders.pdf_loader import load_pdf

def build_faiss_index(embeddings):
    dimension = len(embeddings[0]) # takes the dimensionality(length) of one embedding vector
    index = faiss.IndexFlatL2(dimension) #create a FAISS index that will use L2 distance(Euclidean) to compare vectors of this dimension
    index.add(np.array(embeddings).astype("float32")) #embedding list (already vectors)-> numpy array -> in float32 format(deafult being float64), then add to FAISS index

    return index

def search_index(index, query_embedding, top_k=5):
    """
    Search FAISS index for top_k similar vectors.
    """
    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"),
        top_k
    )
    return indices[0], distances[0]

if __name__ == "__main__":
    documents = load_pdf("data/raw/paper.pdf")
    chunks = chunk_documents(documents)
    embeddings = embed_documents(chunks)

    index = build_faiss_index(embeddings)
    print(f"FAISS index contains {index.ntotal} vectors")

    query = "What are the complications of diabetes?"
    query_embedding = embed_query(query)

    indices, distances = search_index(index, query_embedding)
    print("\n Top relevant chunks: \n")
    for idx in indices:
        print("-" *40)
        print(chunks[idx].page_content[:300])
