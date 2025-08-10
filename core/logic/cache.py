import json
from core.models import Query, Answer, ClauseMapping, Document
from .llm_engine import ask_llm

def check_cache_or_query_llm(query_text, document_id):
    """
    Checks DB for existing LLM response.
    If not found, executes LLM pipeline and stores response.
    """
    document = Document.objects.get(id=document_id)

    # Check if same query already exists
    existing_query = Query.objects.filter(query_text=query_text, document=document).first()
    if existing_query:
        existing_answer = existing_query.answers.first()
        if existing_answer:
            # Cached response
            return {
                "cached": True,
                "query_id": existing_query.id,
                "llm_response": existing_answer.justification,
                "decision": existing_answer.decision,
                "amount": existing_answer.amount
            }

    # Not cached – run LLM pipeline
    result = ask_llm(query_text, pdf_id=document.uin or "bajaj_policy")

    # Safely parse the JSON response instead of eval
    llm_json = json.loads(result["llm_response"])

    # Save to DB
    query_obj = Query.objects.create(query_text=query_text, document=document)
    answer_obj = Answer.objects.create(
        query=query_obj,
        decision=llm_json.get("decision"),
        amount=llm_json.get("amount"),
        justification=llm_json.get("justification")
    )

    # Save clause mappings
    for i, clause in enumerate(result.get("clauses_used", []), 1):
        ClauseMapping.objects.create(
            answer=answer_obj,
            clause_reference=f"Clause {i}",
            clause_text=clause["clause_text"]
        )

    return {
        "cached": False,
        "query_id": query_obj.id,
        "llm_response": answer_obj.justification,
        "decision": answer_obj.decision,
        "amount": answer_obj.amount
    }
