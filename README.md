# 📚 RAG PDF Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_logo.svg)](https://rag-pdf-chatbot-gebiisjhesz6zn2jj6jpfv.streamlit.app/)

A Retrieval-Augmented Generation (RAG) chatbot that allows users to upload their own PDF documents and ask questions about them. The application extracts text from the uploaded PDF, creates vector embeddings, stores them in a FAISS vector database, and uses the Groq Llama 3.3 language model to generate accurate answers based on the document content.

---

## 🚀 Features

- 📄 Upload your own PDF files
- 💬 Chat with the uploaded PDF
- 🔍 Semantic search using FAISS
- 🤖 AI-powered answers using Groq Llama 3.3
- 🧠 Hugging Face sentence-transformer embeddings
- 📜 Chat history during the session
- ⚡ Fast retrieval using vector embeddings
- 📖 View the source chunks used to answer questions
- 🌐 Simple and interactive Streamlit interface

---

## 🛠 Technologies Used

- Python 3.12
- Streamlit
- LangChain
- FAISS
- Hugging Face Embeddings
- Sentence Transformers
- Groq API
- PyMuPDF (fitz)
- Python-dotenv

---

## 📂 Project Structure

```text
rag-pdf-chatbot/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
└── data/
```
⚙ Installation
1. Clone the repository
git clone [https://github.com/Prernasharma04/rag-pdf-chatbot.git](https://github.com/Prernasharma04/rag-pdf-chatbot.git)
cd rag-pdf-chatbot
2. Create a virtual environment
Windows
python -m venv .venv
Activate it:
.venv\Scripts\activate
Mac/Linux
python3 -m venv .venv
Activate it:
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Create a .env file
GROQ_API_KEY=your_groq_api_key_here
Get your API key from the Groq Console.

▶️ Run the application
streamlit run app.py
The application will open automatically in your browser.
How It Works
Upload: Upload a PDF document.

Extract: The application extracts the text using PyMuPDF.

Chunk: The text is split into smaller chunks.

Embed: Hugging Face creates embeddings for each chunk.

Store: FAISS stores the embeddings in a local vector database.

Query: When you ask a question:

Relevant chunks are retrieved using semantic search.

The retrieved context is sent to the Groq Llama model.

The model generates a precise answer based on the retrieved content.

🎯 Future Improvements
Support multiple PDF uploads

Display page numbers as citations

Export chat history

Conversation memory

OCR support for scanned PDFs

👨‍💻 Author
Prerna

Bachelor's Student | AI & Machine Learning Enthusiast

📄 License
This project is licensed under the MIT License.
