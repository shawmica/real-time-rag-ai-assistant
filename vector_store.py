from langchain_chroma import Chroma
from embeddings import get_embeddings

DB_PATH = "chroma_db"

def get_vector_store():

    embeddings = get_embeddings()

    vector_store = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    return vector_store