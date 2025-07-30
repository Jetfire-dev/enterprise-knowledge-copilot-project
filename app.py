# app.py (Streamlit app)
import os
import streamlit as st
from scripts.query_agent import ask_agent, chunks  # ask_agent handles hybrid_search internally

# Streamlit App: Enterprise Knowledge Copilot
st.set_page_config(page_title="Enterprise Knowledge Copilot", layout="wide")
st.title("📚 Enterprise Knowledge Copilot")
st.markdown("Ask questions about the RBI Annual Report 2023-24 and get context-aware answers with citations.")

# Session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar settings
with st.sidebar:
    st.header("Settings")
    k1 = st.slider("Local Retrieval (K1)", min_value=10, max_value=100, value=50)
    k2 = st.slider("OpenAI Re-rank (K2)", min_value=1, max_value=10, value=5)

# User input area
query = st.text_input("Enter your question here:")
if st.button("Ask Copilot") and query:
    with st.spinner("Generating answer..."):
        # Call ask_agent with parameters (handles retrieval and ranking)
        answer, citation_ids = ask_agent(query, k1=k1, k2=k2)
        # Build citation snippets
        citations = []
        for cid in citation_ids:
            snippet = chunks[cid][:200].replace("\n", " ") + '...'
            # Use explicit newline in f-string to avoid unterminated literal
            citations.append(f"> {snippet}  \n[Cited chunk #{cid}]")
        # Save to history
        st.session_state.history.insert(0, {
            "query": query,
            "answer": answer,
            "citations": citations
        })

# Display conversation history
if st.session_state.history:
    st.subheader("Conversation History")
    for entry in st.session_state.history:
        st.markdown(f"**You:** {entry['query']}")
        st.markdown(f"**Copilot:** {entry['answer']}")
        st.markdown("**Citations:**")
        for cite in entry['citations']:
            st.markdown(cite)
        st.write("---")

# Footer
st.markdown("---")
st.markdown("Built with OpenAI GPT-3.5 Turbo, ada-002 embeddings & Sentence-Transformers | Free-tier friendly")