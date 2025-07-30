# Enterprise Knowledge Copilot: RBI Annual Report 2023–24 Q&A Bot

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

4. **Install dependencies**

   pip install -r requirements.txt

5. **Place the RBI PDF in the raw data folder**

   data/raw/rbi_annual_report_2023_24.pdf

6. **Run chunking & indexing**

   python scripts/chunk_and_index.py

7. **Start the Streamlit app**

   streamlit run app.py

## API Key

Create a .env file in the project root:

   OPENAI_API_KEY= your_api_key
