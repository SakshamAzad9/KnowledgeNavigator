# KnowledgeNavigator
Technical Aspects of the AI-Powered Web Search and PDF Question-Answering System with RAG Integration
# AI-Powered Web Search and PDF Question-Answering System

## Overview

The AI-Powered Web Search and PDF Question-Answering System is an innovative solution designed to enhance user interactions with digital information. This project integrates advanced AI models to provide intelligent and contextually relevant responses to user queries. The system is built using Streamlit for the user interface, ensuring an interactive and user-friendly experience.

## Features

- **AI Assistant with Web Search Capabilities:** Allows users to input queries and receive intelligent responses, potentially augmented with up-to-date web search results.
- **PDF Question-Answering:** Upload PDFs and ask questions related to their content, receiving AI-generated answers based on the retrieved information.
- **Retrieval-Augmented Generation (RAG):** Combines retrieval-based and generation-based approaches to enhance the quality and relevance of AI-generated responses.
- **Modular Design:** Easily integrate additional features and improvements, ensuring scalability and adaptability.

## Technical Details

### AI Models

- **Ollama Models:**
  - **`mistral`:** Used for generating responses and making decisions regarding web search necessity and query generation.
  - **`deepseek-r1:8b`:** Employed for tasks such as selecting the best search result and checking the relevance of scraped content.

### PDF Extraction and Processing

- **PDF Loading:** Uses `PDFPlumberLoader` to extract textual content from PDF files.
- **Text Splitting:** Utilizes `RecursiveCharacterTextSplitter` to split PDF text into manageable chunks.
- **Embedding Generation:** Generates embeddings using `OllamaEmbeddings` for semantic search capabilities.
- **Storage:** Stores PDF content chunks as vector embeddings in `InMemoryVectorStore`.

### Web Search and Scraping

- **Search Engine:** Uses DuckDuckGo for performing web searches.
- **HTML Parsing:** Uses BeautifulSoup to parse HTML content and extract search result data.
- **Content Extraction:** Uses Trafilatura to scrape and extract content from web pages.
- **Relevance Checking:** Evaluates the relevance of the scraped content to ensure it aligns with the user's query.

### System Configuration

- **System Messages:** Predefined messages guide the AI models' behavior, ensuring consistent and controlled outputs.
- **Application Launcher:** Allows users to select and run different Streamlit applications.

### User Interface

- **Streamlit:** Provides an interactive web interface for users to engage with the AI applications.

## Installation

### Requirements

- Python 3.8 or later
- Streamlit
- Ollama AI models
- PDFPlumber
- BeautifulSoup
- Trafilatura
- Other dependencies listed in `requirements.txt`

## Install Dependencies:

bash
```
pip install -r requirements.txt
```

## Run the Application:

### To run the AI Assistant with Web Search:
bash
```
streamlit run app.py
```
### To run the PDF Question-Answering System:
bash
```
streamlit run Deep_rag_pdf.py
```
### To use the Application Launcher:
bash
```
streamlit run app2.py
```
### Setup

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
