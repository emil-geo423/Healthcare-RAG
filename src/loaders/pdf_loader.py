from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path

def load_pdf(pdf_path: str):
    """
    Docstring for load_pdf

    :param pdf_path: Description
    :type pdf_path: str
    """
    if not Path(pdf_path).exists():
        raise FileNotFoundError("PDF file not found at: {pdf_path}")
    
    loader = PyPDFLoader(pdf_path) #creates a loader that know how to read the pdf file
    documents = loader.load() #reads the file and splits it into a list of document objects, each document object corresponds to 1 page of the pdf and its content

    return documents

if __name__ == "__main__":
    print("Starting PDF loader...")

    docs = load_pdf("data/raw/paper.pdf")

    print("PDF loaded")
    print(f"Number of documents: {len(docs)}")

    if len(docs) > 0:
        print("\n--- Sample text ---\n")
        print(docs[0].page_content[:500])
    else:
        print("No text extracted from PDF")
