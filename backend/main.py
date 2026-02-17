from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from src.loaders.pdf_loader import load_pdf
from src.processing.chunking import chunk_documents
from src.processing.embeddings import embed_documents, embed_query
from src.rag.vector_store import build_faiss_index, search_index

import ollama

app = FastAPI()

#-------------CORS-------------
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

#-------------GLOBAL STORAGE-------------
SESSIONS = {}

#-------------LLM-------------
def ask__llm(prompt: str):
    response = ollama.chat(
        model="phi3",
        options={"num_ctx": 2048},
        messages = [{
                        "role": "system",
                        "content": "You are a helpful, concise, professional assisstant"},
                    {
                        "role": "user", 
                        "content": prompt}
                    ]
    )
    return response["message"]["content"]

#-------------UPLOAD-------------
@app.post("/upload")
async def upload_pdf(session_id: str, file: UploadFile = File(...)):
    contents = await file.read()
    pdf_path = f"data/raw/{session_id}_{file.filename}"

    with open(pdf_path, "wb") as f:
        f.write(contents)

    documents = load_pdf(pdf_path)

    #ADDING SOURCE METADATA
    for doc in documents:
        doc.metadata["source"] = file.filename

    new_chunks = chunk_documents(documents)

    if session_id not in SESSIONS:
        SESSIONS[session_id]={
            "chunks": [],
            "index": None,
            "history": []
        }
    SESSIONS[session_id]["chunks"].extend(new_chunks)

    embeddings = embed_documents(SESSIONS[session_id]["chunks"])
    index = build_faiss_index(embeddings)

    SESSIONS[session_id]["index"] = index

    return {"fileName": file.filename}

#-------------ASK QUESTION-------------
@app.post("/ask")
def ask_question(session_id: str, question: str):
    if session_id not in SESSIONS:
        return{"error": "Session not found. Upload document first."}
    
    chunks = SESSIONS[session_id]["chunks"]
    index = SESSIONS[session_id]["index"]

    query_embedding = embed_query(question)
    indices,_ = search_index(index, query_embedding, top_k=5)
    context = "\n\n".join([chunks[i].page_content for i in indices])

    #BUILD HISTORY TEXT
    history = SESSIONS[session_id]["history"]
    history_text = ""
    for msg in history[-6:]:
        history_text += f"{msg['role']}: {msg['content']}\n"

    prompt = f"""
You are a medical research assistant.

Formatting rules:
- Use short paragraphs (3-4 lines max).
- If the answer contains multiple items, use bullet points or numbered list
- Use headings when appropriate
- Keep answers concise and well-structured

Conversation so far:
{history_text}

Use ONLY the context below.
If answer not found, say:
"I could not find this information in the provided documents."

Context:
{context}

Question:
{question}
"""

    # Ask Phi-3
    answer = ask__llm(prompt)
  

#SAVING HISTORY
    SESSIONS[session_id]["history"].append(
        {"role": "user", "content": question}
    )
    
    SESSIONS[session_id]["history"].append(
        {"role": "assistant", "content": answer}
    )

    return {"answer": answer}

#-------------RESET-------------
@app.post("/reset")
def reset_session(session_id: str):
    if session_id in SESSIONS:
        del SESSIONS[session_id]
        return{"messgae": "Session reset automatically"}
    return {"message": "Session not found"}