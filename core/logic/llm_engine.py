import cohere
import os
from dotenv import load_dotenv
from .retrieval import search_clauses

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def build_prompt(query, retrieved_clauses):
    """Format prompt for LLM using query and clause texts"""
    prompt = f"""You are a smart insurance policy assistant.

Question:
{query}

Relevant Policy Clauses:
"""

    for i, clause in enumerate(retrieved_clauses, 1):
        prompt += f"\nClause {i}:\n{clause['clause_text']}"

    prompt += """

Now based on the above clauses, answer the question in structured JSON like:
{
  "decision": "approved" or "rejected" or "conditional",
  "amount": "optional - if mentioned",
  "justification": "Why you answered this way, based on which clause",
  "clause_references": ["Clause 1", "Clause 3"]
}
"""

    return prompt.strip()

def ask_llm(query, pdf_id="bajaj_policy"):
    """Final LLM pipeline: query → retrieval → LLM reasoning → JSON"""
    clauses = search_clauses(query, top_k=5, pdf_id=pdf_id)
    prompt = build_prompt(query, clauses)

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        temperature=0.3,
        max_tokens=500
    )

    answer = response.generations[0].text.strip()

    return {
        "query": query,
        "clauses_used": clauses,
        "llm_response": answer
    }
