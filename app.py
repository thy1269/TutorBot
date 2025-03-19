import os
from typing import Optional, List
import streamlit as st
from pathlib import Path
import fitz  # PyMuPDF for PDF handling
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.schema import Document

# Constants
DATA_FOLDER = Path("data")
VECTOR_DB_FOLDER = Path("vector_db")
SUPPORTED_FILE_TYPES = (".txt", ".pdf")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
MODEL_NAME = "gpt-4-turbo"

class KnowledgeBaseManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        DATA_FOLDER.mkdir(exist_ok=True)
        VECTOR_DB_FOLDER.mkdir(exist_ok=True)

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        try:
            with fitz.open(pdf_path) as doc:
                return "\n".join(page.get_text("text") for page in doc)
        except Exception as e:
            st.error(f"Error reading PDF {pdf_path.name}: {e}")
            return ""

    def load_documents(self) -> List[Document]:
        documents = []
        
        for file_path in DATA_FOLDER.iterdir():
            if file_path.suffix not in SUPPORTED_FILE_TYPES:
                continue
                
            try:
                if file_path.suffix == ".txt":
                    loader = TextLoader(str(file_path))
                    docs = loader.load()
                else:  # .pdf
                    pdf_text = self.extract_text_from_pdf(file_path)
                    docs = self.text_splitter.create_documents([pdf_text])
                documents.extend(docs)
            except Exception as e:
                st.error(f"Error processing {file_path.name}: {e}")
                
        if not documents:
            st.warning("No documents found in the knowledge base.")
        return documents

    def create_vector_db(self) -> FAISS:
        documents = self.load_documents()
        return FAISS.from_documents(documents, self.embeddings)

    def load_or_create_vector_db(self) -> Optional[FAISS]:
        try:
            if any(VECTOR_DB_FOLDER.iterdir()):  # Check if folder contains files
                return FAISS.load_local(str(VECTOR_DB_FOLDER), self.embeddings)
        except Exception as e:
            st.error(f"Error loading vector database: {e}")

        vector_db = self.create_vector_db()
        self.save_vector_db(vector_db)
        return vector_db

    def save_vector_db(self, vector_db: FAISS):
        try:
            vector_db.save_local(str(VECTOR_DB_FOLDER))
        except Exception as e:
            st.error(f"Error saving vector database: {e}")

class NLPLearningAssistant:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.kb_manager = KnowledgeBaseManager(api_key)
        self.vector_db = st.cache_resource(self.kb_manager.load_or_create_vector_db)()
        self.retriever = self.vector_db.as_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name=MODEL_NAME, openai_api_key=api_key),
            retriever=self.retriever
        )

    def process_query(self, query: str) -> str:
        with st.spinner("Generating answer..."):
            try:
                return self.qa_chain.run(query)
            except Exception as e:
                st.error(f"Error generating response: {e}")
                return ""

    def update_knowledge_base(self, uploaded_file):
        file_path = DATA_FOLDER / uploaded_file.name
        try:
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            
            with st.spinner("Updating knowledge base..."):
                self.vector_db = self.kb_manager.create_vector_db()
                self.kb_manager.save_vector_db(self.vector_db)
                self.retriever = self.vector_db.as_retriever()
                self.qa_chain.retriever = self.retriever
            st.success("Knowledge base updated!")
        except Exception as e:
            st.error(f"Error updating knowledge base: {e}")

def main():
    api_key = os.getenv("OPENAI_API_KEY", "")
    
    assistant = NLPLearningAssistant(api_key)
    
    st.title("📚 TutorBot")
    st.write("Ask any question related to NLP, and I'll retrieve the best material to answer it!")

    user_query = st.text_input("Type your question here...")
    if user_query:
        response = assistant.process_query(user_query)
        if response:
            st.write("### 🤖 AI Tutor Response:")
            st.write(response)

    uploaded_file = st.file_uploader(
        "Upload NLP Course Materials",
        type=["txt", "pdf"],
        help="Upload text or PDF files to enhance the knowledge base"
    )
    if uploaded_file:
        assistant.update_knowledge_base(uploaded_file)

if __name__ == "__main__":
    main()