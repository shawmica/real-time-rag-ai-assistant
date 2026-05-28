from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

from vector_store import get_vector_store

loader = TextLoader(
    "extracted/fixed_extracted_text.txt",
    encoding="utf-8"
)

documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

vector_store = get_vector_store()

vector_store.add_documents(chunks)

print("Documents embedded successfully!")