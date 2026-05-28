import os
import shutil
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from vector_store import get_vector_store

load_dotenv()

app = FastAPI()

UPLOAD_DIR = "docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

vector_store = get_vector_store()
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

llm = ChatGroq(model="llama-3.3-70b-versatile")

prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant.
Answer using ONLY the provided context.

If the answer is not in the context, say:
"I don't know from the uploaded document."

Context:
{context}

Question:
{question}
""")

class Query(BaseModel):
    question: str


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store
    global retriever

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Delete old document vectors to avoid irrelevant mixed answers
    try:
        vector_store.delete_collection()
    except Exception:
        pass

    # Recreate fresh vector store
    vector_store = get_vector_store()

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documents)

    vector_store.add_documents(chunks)

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 5}
    )

    return {
        "status": "success",
        "message": f"Uploaded and embedded {len(chunks)} chunks from {file.filename}"
    }


@app.post("/ask")
def ask_question(query: Query):
    docs = retriever.invoke(query.question)

    context = "\n\n".join([doc.page_content for doc in docs])

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": query.question
    })

    return {
        "answer": response.content
    }