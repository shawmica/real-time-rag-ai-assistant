import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_PATH = "docs/contract.pdf"
OUTPUT_PATH = "extracted/fixed_extracted_text.txt"

os.makedirs("extracted", exist_ok=True)

loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, #chunk_size Maximum text per chunk
    chunk_overlap=200 #Shared context between chunks
)

chunks = splitter.split_documents(documents)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for i, chunk in enumerate(chunks, start=1):
        f.write(f"\n--- Chunk {i} ---\n")
        f.write(chunk.page_content)
        f.write("\n")

print(f"PDF parsed successfully. Total chunks: {len(chunks)}")