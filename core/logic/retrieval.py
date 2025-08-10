import faiss
import json
import numpy as np
import os
import cohere
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def load_faiss_index(pdf_id="bajaj_policy"):
    """Load FAISS index and clause metadata"""
    index_path = f"embeddings/{pdf_id}.faiss"
    meta_path = f"embeddings/{pdf_id}_clauses.json"

    if not os.path.exists(index_path) or not os.path.exists(meta_path):
        raise FileNotFoundError(f"Missing FAISS or metadata for {pdf_id}")

    index = faiss.read_index(index_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        clauses = json.load(f)

    return index, clauses

def embed_query(query_text):
    """Embed user query using Cohere"""
    response = co.embed(
        texts=[query_text],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    return np.array(response.embeddings).astype("float32")

def search_clauses(query, top_k=5, pdf_id="bajaj_policy"):
    """Search top K matching clauses using semantic similarity"""
    index, clauses = load_faiss_index(pdf_id)
    query_embedding = embed_query(query)

    distances, indices = index.search(query_embedding, top_k)
    results = []

    for i in range(top_k):
        clause_index = indices[0][i]
        similarity_score = float(distances[0][i])
        results.append({
            "clause_index": clause_index,
            "similarity": similarity_score,
            "clause_text": clauses[clause_index]
        })

    return results
