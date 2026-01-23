print(">>> chunking.py: FILE STARTED <<<")

from langchain_text_splitters import RecursiveCharacterTextSplitter
print(">>> Imported RecursiveCharacterTextSplitter <<<")

from src.loaders.pdf_loader import load_pdf
print(">>> Imported load_pdf <<<")


def chunk_documents(documents):
    
    """
    Splits the documents into smaller overlapping chunks
    """
    print(">>> Inside chunk_documents <<<")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )

    chunks = text_splitter.split_documents(documents)
    return chunks

if __name__ == "__main__":
    print(">>> Inside __main__ <<<")

    docs = load_pdf("data/raw/paper.pdf")
    print(f">>> Docs loaded: {len(docs)} <<<")

    chunks = chunk_documents(docs)
    print(f">>> Chunks created: {len(chunks)} <<<")

    print("\n-- Sample chunk--\n")
    print(chunks[0].page_content[:500])