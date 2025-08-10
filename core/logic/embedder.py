import cohere
import faiss
import numpy as np
import json
import os
import time
from .parser import parse_pdf_to_clauses
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

import time
from cohere.errors import TooManyRequestsError

def get_clause_embeddings_in_batches(clauses, batch_size=50, delay=6, max_retries=3):
    all_embeddings = []
    total_batches = (len(clauses) + batch_size - 1) // batch_size

    for i in range(total_batches):
        batch_clauses = clauses[i*batch_size : (i+1)*batch_size]
        print(f"⚡ Embedding batch {i+1} of {total_batches} with {len(batch_clauses)} clauses...")

        retries = 0
        while retries <= max_retries:
            try:
                response = co.embed(
                    texts=batch_clauses,
                    model="embed-english-v3.0",
                    input_type="search_document"
                )
                all_embeddings.extend(response.embeddings)
                break  # success
            except TooManyRequestsError:
                retries += 1
                wait_time = delay * retries
                print(f"⚠️ Rate limit exceeded. Retry {retries}/{max_retries} after {wait_time} seconds...")
                time.sleep(wait_time)
        else:
            raise Exception("Max retries exceeded for embedding batch")

        if i < total_batches - 1:
            time.sleep(delay)  # normal delay between batches

    return all_embeddings

def build_faiss_index(clauses, pdf_id="bajaj_policy"):
    """Build FAISS index from clause embeddings and save index + metadata"""
    embeddings = get_clause_embeddings_in_batches(clauses, batch_size=50, delay=6)
    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))

    os.makedirs("embeddings", exist_ok=True)

    faiss_path = f"embeddings/{pdf_id}.faiss"
    faiss.write_index(index, faiss_path)

    meta_path = f"embeddings/{pdf_id}_clauses.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(clauses, f, indent=2)

    print(f"✅ FAISS index saved to: {faiss_path}")
    print(f"✅ Clause metadata saved to: {meta_path}")

def embed_pdf_to_faiss(pdf_path, pdf_id="bajaj_policy"):
    """Full pipeline: parse PDF → extract clauses → embed → build & save FAISS index"""
    print(f"🔍 Parsing PDF: {pdf_path}")
    clauses = parse_pdf_to_clauses(pdf_path)
    print(f"📄 Extracted {len(clauses)} clauses. Embedding...")
    build_faiss_index(clauses, pdf_id)
