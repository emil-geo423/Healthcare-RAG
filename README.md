Healthcare Research Assistant using RAG

-----------------------------------------
Overview
This project implements a Retrieval-Augmented Generation (RAG) system that answers healthcare-related questions strictly based on uploaded research papers.
Instead of relying on general model knowledge, the system retrieves relevant document sections and generates grounded, non-hallucinated answers.

-----------------------------------------
How the System Works
1. PDF Ingestion – Research papers are loaded and converted into text
2. Chunking – Long documents are split into overlapping chunks
3. Embeddings – Each chunk is converted into semantic vectors
4. Vector Store (FAISS) – Enables fast similarity-based retrieval
5. LLM Generation – A Hugging Face model generates answers using only retrieved context

-----------------------------------------
Architecture
PDF → Chunks → Embeddings → FAISS → Relevant Context → LLM → Answer

-----------------------------------------
Key Features
->Domain-restricted (answers only from uploaded documents)
->Semantic search (not keyword-based)
->Hallucination control using prompt constraints
->Fully offline & free (Hugging Face models)
->Easily extendable to other domains (finance, policy, enterprise)

-----------------------------------------
Tech Stack
-Python
-LangChain
-Hugging Face Transformers
-FAISS
-Sentence Transformers

-----------------------------------------
Use Cases
-Medical research assistance
-Clinical literature review
-Enterprise document QA
-Policy and compliance clarification systems

-----------------------------------------
Disclaimer
THIS SYSTEM IS FOR RESEARCH AND EDUCATIONAL PURPOSE ONLY. DO NOT USE THIS FOR DIAGNOSIS
