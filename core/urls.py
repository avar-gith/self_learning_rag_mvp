#file: core/urls.py
# Fő URL konfiguráció: AI, RAG

from django.urls import path
from core.views import (
    index_view,

    # AI
    ai_test_view,
    chat_view,

    # RAG
    rag_test_view,
    rag_view,
)

urlpatterns = [
    # Főoldal
    path("", index_view, name="index"),

    # AI teszt oldal
    path("ai/test", ai_test_view, name="ai_test"),

    # RAG teszt oldal
    path("ai/rag-test", rag_test_view, name="rag_test"),

    # API végpontok
    path("api/chat", chat_view, name="api_chat"),
    path("api/rag", rag_view, name="api_rag"),

]
