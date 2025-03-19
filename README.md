# Personalized NLP Learning Assistant using RAG

A Retrieval-Augmented Generation (RAG)-based learning assistant for mastering Natural Language Processing (NLP) through interactive, personalized experiences. It retrieves relevant course materials and pairs them with generative AI for contextual explanations.

## Features
- **Document Storage & Retrieval**: Efficiently manages NLP materials using FAISS.
- **RAG Framework**: Combines retrieval with GPT-4 for enhanced responses.
- **Interactive Learning**: Ask questions, get accurate, context-aware answers.
- **Personalization**: Adapts to user learning patterns over time.
- **Document Uploading**: Supports PDFs and text to expand the knowledge base.

## Technologies
- **Python**: Core language
- **Streamlit**: User interface
- **OpenAI GPT-4**: Generative AI
- **FAISS**: Vector storage/retrieval
- **LangChain**: Retrieval + GPT-4 integration
- **PyMuPDF (fitz)**: PDF processing
- **Pickle**: Vector database storage

## Installation

### Prerequisites
- Python 3.8+
- Install dependencies:
  ```bash
  pip install streamlit openai langchain faiss-cpu pymupdf python-dotenv
