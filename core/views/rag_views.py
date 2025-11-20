#file: core/views/rag_views.py
# RAG teszt UI + RAG keresési API végpont.

import json
import markdown
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from services.rag.rag_service import RAGService
from services.rag.prompt_builder import build_prompt
from services.ai_provider import get_ai_client
from knowledge.models import KnowledgeItem


def rag_test_view(request):
    """RAG tesztoldal betöltése."""
    return render(request, "ai/rag_test.html")


@csrf_exempt
def rag_view(request):
    """RAG keresési API végpont."""

    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "POST kérés szükséges."}, status=405)

    try:
        body = json.loads(request.body)

        query = body.get("query", "").strip()
        llm = body.get("llm", "openai")
        top_k = int(body.get("top_k", 5))
        threshold = float(body.get("threshold", 0.35))

        if not query:
            return JsonResponse(
                {"status": "error", "message": "A 'query' mező kötelező."},
                status=400
            )

        # Klasszikus keresés
        classic_items = KnowledgeItem.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(anonymized_content__icontains=query)
        ).order_by("-created_at")[:5]

        classic_results = [
            {
                "title": item.title,
                "snippet": (item.anonymized_content or item.content)[:160] + "..."
            }
            for item in classic_items
        ]

        # Embedding keresés
        rag = RAGService()
        embedding_hits = rag.search(query=query, top_k=top_k, threshold=threshold)

        embedding_results = [
            {
                "chunk": chunk.content,
                "score": score,
                "is_above": score >= threshold
            }
            for chunk, score in embedding_hits
        ]

        # Prompt
        prompt = build_prompt(query=query, rag_results=embedding_hits)

        # LLM hívás
        try:
            client = get_ai_client(llm)
            raw_answer = client.chat(prompt)

            final_answer = markdown.markdown(
                raw_answer,
                extensions=[
                    "markdown.extensions.fenced_code",
                    "markdown.extensions.tables",
                    "markdown.extensions.nl2br",
                    "markdown.extensions.sane_lists",
                ]
            )
        except Exception as e:
            final_answer = f"<strong>Hiba a LLM hívásban:</strong> {e}"

        return JsonResponse({
            "status": "ok",
            "classic_results": classic_results,
            "embedding_results": embedding_results,
            "final_answer": final_answer,
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
