#file: core/views.py
# Nézetek: kezdőoldal és AI chat endpoint, amely Markdown választ HTML-re konvertál.

import json
import markdown
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from services.ai_provider import get_ai_client


# -------------------------------------------------------------------------
# Kezdőoldal
# -------------------------------------------------------------------------
def index_view(request):
    """A projekt főoldala."""
    return render(request, "index.html")


def ai_test_view(request):
    """AI tesztoldal betöltése."""
    return render(request, "ai/test.html")


# -------------------------------------------------------------------------
# Chat API végpont – Markdown → HTML konverzióval
# -------------------------------------------------------------------------
@csrf_exempt
def chat_view(request):
    """
    Chat endpoint:
    - POST kérésben érkezik a kiválasztott LLM és a felhasználói üzenet
    - A megfelelő kliens meghívásra kerül
    - Az LLM válaszát Markdown → HTML formában adjuk vissza
    """

    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "POST kérés szükséges."},
            status=405
        )

    try:
        # JSON dekódolása a fetch() POST-ból
        body = json.loads(request.body)

        llm = body.get("llm")
        message = body.get("message")

        # Validáció
        if not message:
            return JsonResponse(
                {"status": "error", "message": "A 'message' mező kötelező."},
                status=400
            )

        # Megfelelő AI kliens kiválasztása
        client = get_ai_client(llm)

        # Sima (nyers) válasz az LLM-től → általában Markdown formátum
        raw_answer = client.chat(message)

        # -----------------------------------------------------------------
        # Markdown → HTML konverzió
        # -----------------------------------------------------------------
        rendered_answer = markdown.markdown(
            raw_answer,
            extensions=[
                "markdown.extensions.fenced_code",    # kódrészek
                "markdown.extensions.tables",         # táblázatok
                "markdown.extensions.nl2br",          # sortörések
                "markdown.extensions.sane_lists",     # normális listák
            ]
        )

        # A konvertált HTML-t küldjük vissza
        return JsonResponse({
            "status": "ok",
            "provider": llm,
            "answer": rendered_answer,
        })

    except Exception as e:
        # Hibakezelés (JSON válaszban)
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=500
        )
