Lowell

RAG Support Chatbot for Angel One
------------------------------------------------------------------------------------------------------------------

A Retrieval-Augmented Generation (RAG) chatbot trained on Angel One's customer support documentation to assist users by answering queries and providing relevant support information.

## Objective

The primary goal of this project is to develop a specialized chatbot that can accurately answer user questions based "only" on a curated knowledge base. This knowledge base is built from scraping the Angel One support website and ingesting provided PDF documents. The chatbot is designed to be a reliable first line of support, explicitly stating when it does not have enough information to provide an answer.

## Features

Retrieval-Augmented Generation:
Uses a vector database to find relevant context before generating an answer, reducing hallucinations and improving factual accuracy.

Multi-Source Knowledge Base:
Ingests data from both public web pages and private PDF documents.

Strict Contextual Answering:
The chatbot is instructed to answer *only* from the retrieved context. If the answer isn't in the provided sources, it will reply with `I Don't know`.

Interactive UI:
A user-friendly, web-based chat interface built with Streamlit.

## Tech Stack
--------------------------------------------------------------------------------------------------------------------
Language: Python
LLM & Embeddings: Google Gemini (`gemini-1.5-flash-latest` for generation, `embedding-001` for embeddings)
Vector Database: ChromaDB
Web Framework: Streamlit
Data Scraping: Requests & BeautifulSoup4
PDF Processing: PyMuPDF
Text Processing: LangChain (for `RecursiveCharacterTextSplitter`)

--------------------------------------------------------------------------------------------------------------------
## Setup and Installation

Follow these steps to set up the project environment locally.



--->Install Dependencies and API Key
----------------------------------------------------------------------------------------------------------------------
Install all the required Python libraries from the "requirements.txt" file.
pip install -r requirements.txt

Set Up Environment Variable
Create a file named `.env` in the root of the project directory and add your Google API key.

GOOGLE_API_KEY="your_google_api_key_here"


How to Run the Application

The application runs in two main phases: first, building the knowledge base, and second, running the user-facing chatbot.

--------------------------------------------Phase 1: Build the Knowledge Base-----------------------------------------

You must run these scripts in order to populate the "chroma_db" vector database.

1. Place PDF Files
Put all your support PDF documents inside the "data/pdfs/" directory.

2. Run the Data Pipeline Scripts
Execute these scripts one by one from your terminal.

###Scrape the Angel One support website
python src/scraper.py

###Extract text from your PDFs

python src/pdf_ingest.py

###Create the database and embeddings

python src/index_and_embed.py

->Wait for this final script to complete. It will create a "chroma_db" directory in your project folder.

###create the rag_logic file
python src/rag_logic.py

---------------------------------------------Phase 2: Launch the Chatbot-------------------------------------------------

streamlit run src/app.py

Open the local URL provided by Streamlit in your web browser to start chatting.
