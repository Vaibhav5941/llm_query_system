from django.shortcuts import render
from core.models import Document
from core.logic.cache import check_cache_or_query_llm

def ask_question_view(request):
    documents = Document.objects.all()
    context = {"documents": documents}

    if request.method == "POST":
        question = request.POST.get("question")
        document_id = request.POST.get("document_id")

        response = check_cache_or_query_llm(question, document_id=int(document_id))
        context.update({
            "question": question,
            "response": response,
            "selected_doc": int(document_id)
        })

    return render(request, "ask.html", context)
