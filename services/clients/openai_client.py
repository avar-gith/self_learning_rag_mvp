#file: services/clients/openai_client.py
# Egyszerű OpenAI kliens – chat + embedding funkcióval.

from openai import OpenAI
from django.conf import settings
from services.clients.base_client import BaseClient


class OpenAIClient(BaseClient):
    """Chat és embedding hívások az OpenAI API-n keresztül."""

    def __init__(self):
        api_key = settings.OPENAI_SETTINGS.get("api_key")
        if not api_key:
            raise ValueError("❌ OPENAI_API_KEY nincs beállítva!")

        self.chat_model = settings.OPENAI_SETTINGS.get("model", "gpt-4o-mini")
        self.embedding_model = "text-embedding-3-small"

        self.client = OpenAI(api_key=api_key)

        print(f"✅ OpenAIClient inicializálva: chat_model={self.chat_model}")

    def chat(self, prompt: str) -> str:
        """Chat-hívás az OpenAI 'responses' endpointon keresztül."""

        try:
            response = self.client.responses.create(
                model=self.chat_model,
                input=[{"role": "user", "content": prompt}],
                max_output_tokens=2000,
            )

            # Az új OpenAI SDK output_text mezőt ad vissza
            return response.output_text

        except Exception as e:
            return f"Hiba az OpenAI chat hívás során: {e}"

    def get_embedding(self, text: str) -> list:
        """Embedding generálása OpenAI segítségével."""

        try:
            result = self.client.embeddings.create(
                model=self.embedding_model,
                input=text,
            )

            return result.data[0].embedding

        except Exception as e:
            print(f"Hiba embedding közben: {e}")
            return []
