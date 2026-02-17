from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.loaders.pdf_loader import load_pdf

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    
    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        chunk.metadata["page"] = chunk.metadata.get("page", None)
        chunk.metadata["source"] = chunk.metadata.get("source", None)

    return chunks

if __name__ == "__main__":
    documents = load_pdf("data/raw/paper.pdf")
    chunks = chunk_documents(documents)

    print(f"Documetn page count: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")
    print("\n--- Sample Chunk ---\n")
    print(chunks[0].page_content[:500])
    print("\nMetadata: ", chunks[0].metadata)