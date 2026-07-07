import os
import streamlit as st
import fitz
from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

# -----------------------
# Load Environment Variables
# -----------------------

load_dotenv()

groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="Chat with PDF",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Chat with Your PDF")

# -----------------------
# Cache Embedding Model
# -----------------------

@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# -----------------------
# Cache Groq Model
# -----------------------

@st.cache_resource
def load_llm():
    return ChatGroq(
        groq_api_key=groq_api_key,
        model="llama-3.3-70b-versatile",
        temperature=0
    )

embeddings = load_embeddings()
llm = load_llm()

# -----------------------
# Session State
# -----------------------

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# Sidebar
# -----------------------

st.sidebar.title("📄 Upload PDF")

uploaded_file = st.sidebar.file_uploader(
    "Choose a PDF",
    type="pdf"
)

# -----------------------
# Process PDF
# -----------------------

if uploaded_file is not None:

    if st.session_state.pdf_name != uploaded_file.name:

        with st.spinner("Reading PDF..."):

            pdf = fitz.open(
                stream=uploaded_file.read(),
                filetype="pdf"
            )

            text = ""

            for page in pdf:
                text += page.get_text()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_text(text)

        with st.spinner("Creating Vector Database..."):

            vector_store = FAISS.from_texts(
                chunks,
                embedding=embeddings
            )

        st.session_state.vector_store = vector_store
        st.session_state.pdf_name = uploaded_file.name
        st.session_state.messages = []

        st.sidebar.success("✅ PDF Ready!")
        st.sidebar.write(f"Chunks: {len(chunks)}")

# -----------------------
# Display Chat History
# -----------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------
# Chat
# -----------------------

if st.session_state.vector_store:

    question = st.chat_input("Ask anything about your PDF...")

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        docs = st.session_state.vector_store.similarity_search(
            question,
            k=3
        )

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        prompt = f"""
You are a helpful assistant.

Answer ONLY using the context below.

If the answer is not found, reply:

I don't know.

Context:
{context}

Question:
{question}
"""

        with st.spinner("Thinking..."):

            response = llm.invoke(prompt)

            answer = response.content

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):

            st.markdown(answer)

            with st.expander("📄 Source Chunks"):

                for i, doc in enumerate(docs):

                    st.write(f"Chunk {i+1}")

                    st.info(doc.page_content)

else:

    st.info("👈 Upload a PDF from the sidebar to begin chatting.")
