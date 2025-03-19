# TutorBot

 Personalised Learning Assistant using RAG

This project is a Retrieval-Augmented Generation (RAG)-based learning assistant designed to help users learn Natural Language Processing (NLP) through an interactive and personalized experience. The system retrieves the most relevant course materials and combines them with generative AI capabilities to provide clear and context-aware explanations.


# Overview:

This project is a Retrieval-Augmented Generation (RAG)-based learning assistant designed to help users learn Natural Language Processing (NLP) through an interactive and personalized experience. The system retrieves the most relevant course materials and combines them with generative AI capabilities to provide clear and context-aware explanations.

Features

Document Storage & Retrieval: Uses FAISS (Facebook AI Similarity Search) to store and retrieve NLP course materials efficiently.

RAG Framework: Enhances learning by combining document retrieval with GPT-4's language generation capabilities.

Interactive Learning: Users can ask questions and receive accurate, contextual responses.

Personalization: Adapts to user learning patterns, tailoring recommendations over time.

Document Uploading: Supports PDF and text-based course materials, allowing dynamic knowledge base expansion.

Technologies Used

Python (Primary language)

Streamlit (For the user interface)

OpenAI GPT-4 (For generative AI responses)

FAISS (For vector-based document storage and retrieval)

LangChain (To integrate retrieval-based search with GPT-4)

PyMuPDF (fitz) (For processing PDFs)

Pickle (For storing and loading the vector database)

Installation

Prerequisites

Ensure you have Python 3.8+ installed. Then, install the required dependencies:

pip install streamlit openai langchain faiss-cpu pymupdf python-dotenv

Setting Up OpenAI API Key

Set your OpenAI API key as an environment variable:

setx OPENAI_API_KEY "your_openai_api_key"

Or, create a .env file in the project directory:

OPENAI_API_KEY=your_openai_api_key

How to Run

Place your NLP course materials inside the data/ folder.

Run the Streamlit application:

streamlit run app.py

Enter your question in the UI, and the assistant will provide an answer based on retrieved documents.

(Optional) Upload additional NLP course materials in PDF or text format.

File Structure

📂 project_root/
├── 📂 data/                   # Folder for storing NLP course materials
├── 📜 app.py                  # Main Streamlit app
├── 📜 vector_db.pkl           # Pickled FAISS vector database
├── 📜 README.md               # Project documentation
├── 📜 .env                     # Environment variables (e.g., API keys)

Future Enhancements

Implement user authentication to store learning progress.

Support multimodal learning (text, images, and videos).

Enhance response personalization using fine-tuned models.
