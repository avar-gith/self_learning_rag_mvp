#file: services/ai_provider.py
# A modul a megfelelő AI klienst adja vissza llm paraméter alapján.

from services.clients.pluto_client import PlutoAIClient
from services.clients.openai_client import OpenAIClient
from services.clients.perplexity_client import PerplexityClient


def get_ai_client(llm: str):
    """
    Visszaadja a megfelelő AI klienst a megadott llm alapján.
    Engedélyezett értékek:
    - pluto
    - openai
    - perplexity
    """
    llm = (llm or "").lower()

    if llm == "pluto":
        return PlutoAIClient()

    if llm == "openai":
        return OpenAIClient()

    if llm == "perplexity":
        return PerplexityClient()

    raise ValueError(f"❌ Ismeretlen LLM provider: {llm}")
