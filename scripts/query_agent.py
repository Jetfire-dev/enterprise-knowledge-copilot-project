
import os
import faiss
import pickle
import numpy as np
import hashlib
import re
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# 1) Load environment & API client
load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 2) Define paths for index, chunks, and cache
BASE_DIR    = os.path.dirname(__file__)
INDEX_DIR   = os.path.abspath(os.path.join(BASE_DIR, '../data/index'))
LOCAL_INDEX = os.path.join(INDEX_DIR, "local_faiss.index")
CHUNKS_FILE = os.path.join(INDEX_DIR, "chunks.pkl")
CACHE_PATH  = os.path.join(INDEX_DIR, "ada_cache.pkl")

# 3) Initialize or load cache
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, "rb") as f:
        ada_cache = pickle.load(f)
else:
    ada_cache = {}

# 4) Cached OpenAI embedding function
def get_ada_embedding(text: str):
    key = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if key in ada_cache:
        return ada_cache[key]
    resp = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    emb = resp.data[0].embedding
    ada_cache[key] = emb
    with open(CACHE_PATH, "wb") as f:
        pickle.dump(ada_cache, f)
    return emb

# 5) Load FAISS index and chunk list
local_index = faiss.read_index(LOCAL_INDEX)
with open(CHUNKS_FILE, "rb") as f:
    chunks = pickle.load(f)

# 6) Local embedder
st_model = SentenceTransformer("all-MiniLM-L6-v2")

# 7) Helper: filter for chunks containing percentage patterns (%, percent, per cent)
def filter_percent_chunks(candidates):
    pct_pattern = re.compile(r"\d+(?:\.\d+)?\s*(?:%|percent|per\s*cent)", re.IGNORECASE)
    return [(text, idx) for text, idx in candidates if pct_pattern.search(text)]

# 8) Hybrid search: return list of (chunk_text, original_index)
def hybrid_search(query: str, k1: int = 50, k2: int = 5):
    q_emb_local = st_model.encode([query])
    _, local_ids = local_index.search(np.array(q_emb_local).astype("float32"), k1)
    candidates = [(chunks[i], i) for i in local_ids[0]]

    ada_embs = [get_ada_embedding(text) for text, _ in candidates]
    dim = len(ada_embs[0])
    refine_index = faiss.IndexFlatL2(dim)
    refine_index.add(np.array(ada_embs).astype("float32"))

    q_ada = get_ada_embedding(query)
    _, refine_ids = refine_index.search(np.array([q_ada]).astype("float32"), k2)
    return [candidates[i] for i in refine_ids[0]]

# 9) Ask agent: filters for relevant numeric chunks, no fallback to ensure strict citation
def ask_agent(query: str, k1: int = 50, k2: int = 5):
    top = hybrid_search(query, k1=k1, k2=k2)
    filtered = filter_percent_chunks(top)
    if not filtered:
        return "Sorry, I couldn’t find any exact percentage data in the report.", []

    citation_ids = [idx for _, idx in filtered]
    system = (
        "You are an expert assistant. Use only the provided excerpts to answer accurately. "
        "Cite only those excerpts that directly contain the numbers you mention."
    )
    formatted = "\n\n".join(f"[{idx}] {chunk}" for chunk, idx in filtered)
    user_content = formatted + f"\n\nQuestion: {query}"

    resp = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user_content}
        ]
    )
    answer = resp.choices[0].message.content
    return answer, citation_ids

