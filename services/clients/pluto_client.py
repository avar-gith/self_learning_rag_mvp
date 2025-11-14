#file: services/clients/pluto_client.py
# PlutoAI kliens – OpenAI "responses" kompatibilis adapterrel.

import requests
from django.conf import settings
from services.clients.base_client import BaseClient


class PlutoAIClient(BaseClient):
    """Egyszerű kliens a PlutoAI szolgáltatás használatához (OpenAI responses adapter)."""

    def __init__(self):
        self.api_key = settings.PLUTOAI_SETTINGS.get("api_key")
        self.base_url = settings.PLUTOAI_SETTINGS.get("base_url")
        self.model = settings.PLUTOAI_SETTINGS.get("model")
        self.verify_ssl = settings.PLUTOAI_SETTINGS.get("verify_ssl", False)

        if not self.api_key:
            raise ValueError("❌ PLUTOAI_API_KEY nincs beállítva az .env-ben!")

        print(f"✅ PlutoAIClient inicializálva: model={self.model}")

    def chat(self, prompt: str) -> str:
        """Chat hívás a PlutoAI /v1/responses adapter endpointján."""

        url = f"{self.base_url}/v1/responses"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "input": [
                {"role": "user", "content": prompt}
            ],
            "max_output_tokens": 2000,
            "temperature": 0.3
        }

        resp = requests.post(
            url, json=payload, headers=headers, verify=self.verify_ssl
        )

        if resp.status_code != 200:
            raise RuntimeError(f"PlutoAI API hiba ({resp.status_code}): {resp.text}")

        data = resp.json()

        # A PlutoAI "responses" output szerkezete:
        # data["output"][0]["content"][0]["text"]
        try:
            return data["output"][0]["content"][0]["text"]
        except Exception:
            return str(data)
