#file: core/views/ai_views.py
# AI chat nézetek: UI + API végpont.

import json
import markdown
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from services.ai_provider import get_ai_client


def ai_test_view(request):
    """AI tesztoldal betöltése."""
    return render(request, "ai/test.html")


@csrf_exempt
def chat_view(request):
    """Egyszerű chat végpont LLM-ekhez."""

    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "POST kérés szükséges."},
            status=405
        )

    try:
        body = json.loads(request.body)

        llm = body.get("llm")
        message = body.get("message")

        if not message:
            return JsonResponse(
                {"status": "error", "message": "A 'message' mező kötelező."},
                status=400
            )

        client = get_ai_client(llm)
        raw_answer = client.chat(message)

        rendered = markdown.markdown(
            raw_answer,
            extensions=[
                "markdown.extensions.fenced_code",
                "markdown.extensions.tables",
                "markdown.extensions.nl2br",
                "markdown.extensions.sane_lists",
            ]
        )

        return JsonResponse({
            "status": "ok",
            "provider": llm,
            "answer": rendered,
        })

    except Exception as e:
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=500
        )
