from django.urls import path
from core.views import index_view, chat_view, ai_test_view

urlpatterns = [
    path("", index_view, name="index"),
    path("api/chat", chat_view, name="api_chat"),
    path("ai/test", ai_test_view, name="ai_test"),
]
