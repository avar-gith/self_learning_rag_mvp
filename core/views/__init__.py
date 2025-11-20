#file: core/views/__init__.py

from .base_views import index_view
from .ai_views import ai_test_view, chat_view
from .rag_views import rag_test_view, rag_view

__all__ = [
    "index_view",
    "ai_test_view",
    "chat_view",
    "rag_test_view",
    "rag_view",
]
