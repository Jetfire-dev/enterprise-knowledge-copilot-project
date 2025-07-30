# Enterprise Knowledge Copilot: RBI Annual Report 2023–24 Q&A Bot

A local chatbot app that answers questions from the **RBI Annual Report 2023–24**, using PDF chunking, vector embeddings, and OpenAI LLMs — all in a lightweight Streamlit interface.

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

2. **Create and activate a virtual environment**

   python -m venv venv
   source venv/bin/activate

3. **Install dependencies**

   pip install -r requirements.txt

4. **Place the RBI PDF in the raw data folder**

   data/raw/rbi_annual_report_2023_24.pdf

5. **Run chunking & indexing**

   python scripts/chunk_and_index.py

6. **Start the Streamlit app**

   streamlit run app.py

## API Key

Create a .env file in the project root:

   OPENAI_API_KEY= your_api_key
