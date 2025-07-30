# scripts/chunk_and_index.py
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
INPUT_TEXT = "data/raw/all_text.txt"
INDEX_DIR  = "data/index"
INDEX_FILE = os.path.join(INDEX_DIR, "local_faiss.index")
CHUNKS_FILE= os.path.join(INDEX_DIR, "chunks.pkl")

# Parameters
CHUNK_SIZE = 500  # approx chars per chunk
MODEL_NAME = "all-MiniLM-L6-v2"

def split_text(text, chunk_size=CHUNK_SIZE):
    paras, chunks, curr = text.split("\n\n"), [], ""
    for p in paras:
        if len(curr) + len(p) < chunk_size:
            curr += p + "\n\n"
        else:
            chunks.append(curr.strip())
            curr = p + "\n\n"
    if curr: chunks.append(curr.strip())
    return chunks

def main():
    os.makedirs(INDEX_DIR, exist_ok=True)
    text = open(INPUT_TEXT, "r", encoding="utf-8").read()
    chunks = split_text(text)
    print(f"[+] {len(chunks)} chunks generated.")

    # Local embedder
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(chunks, show_progress_bar=True)
    dim = embeddings.shape[1]

    # Build FAISS index
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))

    # Persist
    with open(CHUNKS_FILE, "wb") as f: pickle.dump(chunks, f)
    faiss.write_index(index, INDEX_FILE)
    print(f"[+] Saved local index → {INDEX_FILE}")

if __name__ == "__main__":
    main()
