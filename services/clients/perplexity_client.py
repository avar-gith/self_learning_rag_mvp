#file: services/clients/perplexity_client.py
# Egyszerű Perplexity kliens – HTTP API wrapper (Perplexity chat).

import requests
from django.conf import settings
from services.clients.base_client import BaseClient


class PerplexityClient(BaseClient):
    """Egyszerű kliens a Perplexity API-hoz."""

    def __init__(self):
        self.api_key = settings.PERPLEXITY_SETTINGS.get("api_key")
        self.base_url = settings.PERPLEXITY_SETTINGS.get("base_url", "https://api.perplexity.ai")

        if not self.api_key:
            raise ValueError("❌ PER_API_KEY nincs beállítva!")

        print("✅ PerplexityClient inicializálva")

    def chat(self, prompt: str) -> str:
        """Chat kérése a Perplexity API-hoz."""

        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "sonar",   # <-- Egyetlen biztos, univerzálisan engedett modell
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(
                f"Perplexity API hiba ({response.status_code}): {response.text}"
            )

        data = response.json()
        return data["choices"][0]["message"]["content"]
