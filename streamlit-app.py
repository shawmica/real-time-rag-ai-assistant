import os
import requests
import streamlit as st

WELCOME_MESSAGE = (
    "Hi! Ask me anything about your uploaded document and I will answer "
    "using the relevant retrieved context."
)
DEFAULT_BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="RAG AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes softPulse {
        0% { box-shadow: 0 0 0 0 rgba(127, 23, 52, 0.18); }
        70% { box-shadow: 0 0 0 10px rgba(127, 23, 52, 0); }
        100% { box-shadow: 0 0 0 0 rgba(127, 23, 52, 0); }
    }
    .stApp {
        background: linear-gradient(135deg, #ffffff 0%, #fff7f8 55%, #fdecef 100%);
        color: #3b1f27;
        animation: fadeInUp 0.45s ease-out;
    }
    .stAppViewContainer,
    [data-testid="stAppViewContainer"],
    .main,
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background: transparent !important;
    }
    [data-testid="stBottomBlockContainer"] {
        background: #ffffff !important;
        border-top: 1px solid rgba(128, 26, 52, 0.2);
    }
    .stApp, .stApp p, .stApp li, .stApp label, .stApp span, .stApp div {
        color: #3b1f27;
    }
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown strong {
        color: #3b1f27 !important;
    }
    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0);
    }
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="stFileUploader"] {
        background: #fff8fa;
        border: 1px dashed rgba(128, 26, 52, 0.35);
        border-radius: 10px;
        padding: 0.4rem;
        transition: all 0.22s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(128, 26, 52, 0.6);
        background: #fff3f6;
    }
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] div {
        color: #6b1029 !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] div,
    [data-testid="stFileUploaderDropzoneInstructions"] span {
        color: #6b1029 !important;
        opacity: 1 !important;
        font-weight: 500 !important;
    }
    [data-testid="stFileUploader"] section button {
        background: #fff7f8 !important;
        color: #6b1029 !important;
        border: 1px solid rgba(107, 16, 41, 0.25) !important;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        border: 1px solid rgba(128, 26, 52, 0.2);
        background: #7f1734;
        color: #fff7f8 !important;
        transition: transform 0.18s ease, box-shadow 0.2s ease, background 0.2s ease;
    }
    .stButton > button * {
        color: #fff7f8 !important;
        opacity: 1 !important;
    }
    .stButton > button:hover {
        background: #6b1029;
        color: #ffffff;
        transform: translateY(-1px);
        box-shadow: 0 8px 16px rgba(127, 23, 52, 0.22);
    }
    .stButton > button:disabled {
        background: #f3d7df !important;
        color: #7a3a4b !important;
        border: 1px solid rgba(128, 26, 52, 0.25) !important;
        opacity: 1 !important;
    }
    [data-testid="stChatInput"] {
        background: #ffffff;
        border: 1px solid rgba(128, 26, 52, 0.3);
        border-radius: 10px;
        animation: softPulse 2.2s ease-out 1;
    }
    [data-testid="stChatInput"] > div {
        background: transparent !important;
    }
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] input {
        color: #3b1f27 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInput"] input::placeholder {
        color: #8f4c5d !important;
        opacity: 1 !important;
    }
    [data-testid="stChatInput"] button {
        color: #7f1734 !important;
    }
    .caption-soft {
        color: #7f1734;
        font-size: 0.86rem;
    }
    [data-testid="stChatMessage"] {
        border-radius: 10px;
        border: 1px solid rgba(128, 26, 52, 0.2);
        background: rgba(255, 255, 255, 0.88);
        margin-bottom: 0.45rem;
        padding: 0.08rem 0.5rem 0.25rem 0.5rem;
        transition: transform 0.15s ease, box-shadow 0.2s ease;
        animation: fadeInUp 0.35s ease-out;
    }
    [data-testid="stChatMessage"]:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(127, 23, 52, 0.12);
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: #3b1f27 !important;
    }
    .stCaption, .stCaption p {
        color: #6b2a3b !important;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary * {
        color: #5a1025 !important;
        font-weight: 600 !important;
    }
    [data-testid="stExpander"] {
        border: 1px solid rgba(128, 26, 52, 0.15);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.65);
        animation: fadeInUp 0.5s ease-out;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_server_root(url: str) -> str:
    root = url.strip().rstrip("/")
    if root.endswith("/ask"):
        root = root[: -len("/ask")]
    if root.endswith("/upload"):
        root = root[: -len("/upload")]
    return root


def initialize_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
    if "last_prompt" not in st.session_state:
        st.session_state.last_prompt = ""


initialize_state()

st.title("RAG AI Assistant")
st.caption("Ask questions from your uploaded document.")

server_root = get_server_root(DEFAULT_BACKEND_URL)
ask_url = f"{server_root}/ask"
upload_url = f"{server_root}/upload"

with st.expander("Controls", expanded=True):
    left_col, right_col = st.columns([2, 1])

    with left_col:
        uploaded_file = st.file_uploader(
            "Upload a PDF document",
            type=["pdf"],
            help="Upload a PDF to add document content to the knowledge base.",
        )
        ingest_clicked = st.button(
            "Ingest PDF",
            disabled=uploaded_file is None,
            use_container_width=False,
        )

    with right_col:
        st.write("")
        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": WELCOME_MESSAGE}]
            st.session_state.last_prompt = ""
            st.rerun()

    if uploaded_file and ingest_clicked:
        try:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type or "application/pdf",
                )
            }
            with st.spinner("Ingesting document..."):
                upload_response = requests.post(upload_url, files=files, timeout=90)
                upload_response.raise_for_status()
                result = upload_response.json()

            if result.get("status") == "success":
                message = result.get("message", "PDF uploaded successfully.")
                st.success(message)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": f"Uploaded `{uploaded_file.name}` successfully. {message}",
                    }
                )
            else:
                st.error(result.get("message", "Upload failed."))
        except requests.RequestException as error:
            st.error(f"Upload failed: {error}")

    st.markdown("**Quick starters**")
    sample_questions = [
        "What is this document about?",
        "Summarize the most important points.",
        "What problem does this document solve?",
        "List the top 5 key findings.",
    ]
    starter_cols = st.columns(2)
    for index, prompt in enumerate(sample_questions):
        with starter_cols[index % 2]:
            if st.button(prompt, key=f"quick_{prompt}", use_container_width=True):
                st.session_state.last_prompt = prompt

    st.markdown(
        '<div class="caption-soft">Tip: keep questions short and specific.</div>',
        unsafe_allow_html=True,
    )

typed_question = st.chat_input("Ask a question from your document...")
if st.session_state.last_prompt:
    user_question = st.session_state.last_prompt
    st.session_state.last_prompt = ""
else:
    user_question = typed_question

chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})
    with chat_container:
        with st.chat_message("user"):
            st.write(user_question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    ask_url,
                    json={"question": user_question},
                    timeout=45,
                )
                response.raise_for_status()
                answer = response.json().get("answer", "No answer returned.")
            except requests.RequestException as error:
                answer = (
                    "I could not contact the backend right now. "
                    "Please verify the endpoint and ensure the API server is running.\n\n"
                    f"Error: {error}"
                )
            st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
