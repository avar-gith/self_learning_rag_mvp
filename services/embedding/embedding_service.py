
#file: services/embedding/embedding_service.py
# EmbeddingService – általános embedding generáló modul RAG rendszerekhez.
# Moduláris felépítés: többfajta modellklienssel is működik (OpenAI, PlutoAI stb.).

from typing import List, Optional
from django.conf import settings


class EmbeddingService:
    """
    EmbeddingService
    ----------------
    Egységes interfészt biztosít az embedding generáláshoz.
    A konkrét modellkliens kívülről érkezik (OpenAI, PlutoAI stb.),
    így a szolgáltatás könnyen cserélhető és bővíthető.

    Használat:
        service = EmbeddingService(client=openai_client)
        vector = service.create_embedding("valamilyen szöveg")
    """

    def __init__(self, client):
        """
        Inicializáló metódus.

        Paraméterek:
            client (BaseClient): Olyan kliens, amely rendelkezik
                                 a get_embedding(text) metódussal.
        """
        self.client = client
        self.max_text_length = getattr(settings, "EMBEDDING_MAX_TEXT", 5000)

    def _prepare_text(self, text: str) -> str:
        """
        Szöveg előkészítése embedding generálás előtt.
        Egyszerű MVP: levágjuk, ha túl hosszú.
        Később: anonimizálás, normalizálás, tisztítás.
        """
        text = text.strip()

        if len(text) > self.max_text_length:
            text = text[: self.max_text_length]

        return text

    def create_embedding(self, text: str) -> Optional[List[float]]:
        """
        Embedding generálása a beállított modellklienssel.

        Visszatér:
            - embedding vektor listaként
            - None, ha hiba történik
        """
        if not text or not text.strip():
            return None

        try:
            prepared = self._prepare_text(text)
            vector = self.client.get_embedding(prepared)
            return vector

        except Exception as e:
            print(f"Hiba embedding generálás közben: {e}")
            return None


# -------------------------------------------------------------------------
# Helper – egyszerű hívás külön példányosítás nélkül
# -------------------------------------------------------------------------
def generate_embedding(text: str, client) -> Optional[List[float]]:
    """
    Gyors segítség a külső hívásokhoz.

    Paraméterek:
        text (str): A szöveg, amelyből embedding készül
        client (BaseClient): OpenAIClient vagy PlutoAIClient

    Visszaad:
        embedding vektor vagy None
    """
    service = EmbeddingService(client)
    return service.create_embedding(text)
