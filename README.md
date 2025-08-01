# Enterprise Knowledge Copilot: RBI Annual Report 2023–24 Q&A Bot

## Project Overview

This project is an LLM-powered Q&A agent that answers user questions from the RBI Annual Report 2023–24 using semantic search and OpenAI. Designed as a prototype for enterprise knowledge assistants.

## Features

- Uploads and processes the RBI report (`rbi_annual_report_2023_24.pdf`)
- Uses FAISS for semantic search over document chunks
- GPT-based agent answers your financial/economic queries
- Clean Streamlit interface
- Local `.env` for API key security

## Setup

1. **Clone the repo**

   git clone https://github.com/Jetfire-dev/enterprise-knowledge-copilot-project.git
   
   cd enterprise-knowledge-copilot-project

3. **Create and activate a virtual environment**

   python -m venv venv
   
   source venv/bin/activate

5. **Install dependencies**

   pip install -r requirements.txt

6. **Place the RBI PDF in the raw data folder**

   data/raw/rbi_annual_report_2023_24.pdf

7. **Run chunking & indexing**

   python scripts/chunk_and_index.py

8. **Start the Streamlit app**

   streamlit run app.py

## API Key

Create a .env file in the project root:

   OPENAI_API_KEY= your_api_key

## Limitations

Single Source knowledge-
**This AI agent only knows what’s in the RBI Annual Report 2023–24 PDF.**

No Live Updates- 
**It won’t reflect any data released after the report’s publication date.**


## Extension of AI Agent Project 

If you’d like to experiment with new or additional documents, simply:

1- **Place your new PDF(s) in data/raw/ location (e.g. data/raw/another_report.pdf).**

2- **Re‑run the chunking & indexing step:**

   python scripts/chunk_and_index.py

   This will ingest all PDFs in data/raw/ at once.

3- **Restart the Streamlit app to query over the expanded knowledge base:**

   streamlit run app.py


## Source

The RBI Annual Report 2023–24 used in this project is publicly available from the Reserve Bank of India’s official website:
https://www.rbi.org.in → Publications → Annual Reports


## Disclaimer
This project is for educational and demonstration purposes only. All content from the RBI Annual Report 2023–24 remains the property of the Reserve Bank of India. No commercial use is intended.
