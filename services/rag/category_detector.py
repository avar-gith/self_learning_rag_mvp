#file: services/rag/category_detector.py
# Kategóriadetektálás LLM segítségével – a felhasználói kérdés alapján.

import json
import re
from services.ai_provider import get_ai_client
from knowledge.models import KnowledgeCategory


class CategoryDetector:
    """
    CategoryDetector
    ----------------
    LLM-alapú kategória felismerést végez.
    A rendszer dinamikusan lekérdezi a tudásbázis kategóriáit,
    majd az LLM kiválasztja a leginkább relevánsat.
    """

    def __init__(self, llm_provider: str = "openai"):
        self.client = get_ai_client(llm_provider)

    # ------------------------------------------------------------------
    def get_category_list(self):
        """
        Lekéri az adatbázisból az aktuális kategóriákat.
        """
        return list(KnowledgeCategory.objects.values_list("name", flat=True))

    # ------------------------------------------------------------------
    def build_prompt(self, query: str, categories: list[str]) -> str:
        """
        LLM prompt felépítése.
        A válasz kizárólag JSON lehet:
        {"category": "..."}
        """
        categories_text = "\n".join(f"- {c}" for c in categories)

        return f"""
A feladatod: a felhasználói kérdéshez válaszd ki a leginkább megfelelő kategóriát.

Kérdés:
\"\"\"{query}\"\"\" 

Elérhető kategóriák:
{categories_text}

Fontos szabályok:
- Csak az adott listából választhatsz.
- A válasz kizárólag JSON legyen, ilyen formában:
  {{"category": "Kiválasztott kategória neve"}}
- Ha nem egyértelmű, akkor is válassz a listából.

Most add meg a JSON választ.
"""

    # ------------------------------------------------------------------
    def detect_category(self, query: str) -> str:
        """
        Teljes kategóriadetektálási folyamat:
        - lekérdezi a kategóriákat
        - promptot épít
        - LLM-mel kategóriát választ
        - biztonságos JSON-ként visszaadja az eredményt
        """
        categories = self.get_category_list()
        if not categories:
            return "Ismeretlen (nincs kategória)"

        prompt = self.build_prompt(query, categories)

        try:
            raw = self.client.chat(prompt)

            # ----------------------------------------------------------
            # JSON kivágása az LLM válaszból
            # ----------------------------------------------------------
            json_match = re.search(r"{.*?}", raw, flags=re.DOTALL)
            if not json_match:
                print(f"[CategoryDetector] Hiba: JSON nem található a válaszban -> {raw}")
                return "Ismeretlen (hiba)"

            json_text = json_match.group(0)

            data = json.loads(json_text)
            category = data.get("category")

            # Validáció
            if category in categories:
                return category

            print(f"[CategoryDetector] Hiba: '{category}' nem szerepel a kategórialistában.")
            return "Ismeretlen (érvénytelen kategória)"

        except Exception as e:
            print(f"[CategoryDetector] Hiba: {e}")
            return "Ismeretlen (hiba)"
