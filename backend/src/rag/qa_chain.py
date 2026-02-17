from transformers import pipeline
from src.processing.embeddings import embed_query
from src.rag.vector_store import search_index

llm = pipeline(
    task="question-answering",
    model = "distilbert-base-uncased-distilled-squad",
)

def build_context(chunks, indices):
    
    context=[]
    sources = set()

    for idx in indices:
        context.append(chunks[idx].page_content)

        src = chunks[idx].metadata.get("source")
        page = chunks[idx].metadata.get("page")
        if src:
            sources.add(f"{src} (page {page})")

    return "\n\n".join(context), list(sources)

def ask_question(question, chunks, index):
    query_embedding = embed_query(question)
    indices,_ = search_index(index, query_embedding, top_k=5)

    context, sources = build_context(chunks, indices)

    prompt = f"""
You are a medical research assistant.
Answer the questions ONLY using the context below.
If the answer is not present in the context, say:
"I could not find this information in the provided documents."ImportError

Context:
{context}

Question:
{question}
"""
    
    response = llm(
    question=question,
    context=context
)
    return response["answer"]