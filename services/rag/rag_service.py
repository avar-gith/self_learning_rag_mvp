#file: services/rag/rag_service.py
# RAG kereső szolgáltatás – embedding alapú hasonlóság keresés
# Klasszikus RAG működés: cosine similarity, threshold, top-k visszaadás.

from typing import List, Tuple
import numpy as np
from django.db.models import QuerySet

from services.embedding.embedding_service import EmbeddingService
from services.ai_provider import get_ai_client
from knowledge.models import KnowledgeEmbedding, KnowledgeChunk


# -------------------------------------------------------------------------
# Alapértelmezett RAG paraméterek
# -------------------------------------------------------------------------
DEFAULT_TOP_K = 5
DEFAULT_SIMILARITY_THRESHOLD = 0.35


# -------------------------------------------------------------------------
# Koszinusz hasonlóság számítás
# -------------------------------------------------------------------------
def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Két embedding vektor koszinusz hasonlóságát számítja ki.
    Ha bármelyik vektor érvénytelen, 0.0 értéket ad vissza.
    """
    try:
        a = np.array(vec_a, dtype=float)
        b = np.array(vec_b, dtype=float)
    except Exception:
        return 0.0

    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0

    return float(np.dot(a, b) / denom)


# -------------------------------------------------------------------------
# RAG szolgáltatás – embedding alapú hasonlóság keresés
# -------------------------------------------------------------------------
class RAGService:
    """
    RAGService
    ---------
    Embedding alapú hasonlóság keresést végez a tudásbázis chunkjai között.
    A keresési paraméterek (top_k és threshold) felhasználói oldalon állíthatók.
    """

    def __init__(self, embedding_client=None):
        """
        Inicializálás:
        - embedding_client: OpenAI vagy más embedding kliens
        """
        if embedding_client is None:
            # Alapértelmezés: OpenAI embedding
            embedding_client = get_ai_client("openai")

        self.embedding_service = EmbeddingService(embedding_client)

    # ---------------------------------------------------------------------
    def _get_query_embedding(self, query: str):
        """
        A felhasználói kérdés embeddingjének előállítása.
        Hiba esetén None-t ad vissza.
        """
        try:
            return self.embedding_service.create_embedding(query)
        except Exception as e:
            print(f"[RAG] Hiba a query embedding generálásakor: {e}")
            return None

    # ---------------------------------------------------------------------
    def _get_all_embeddings(self) -> QuerySet:
        """
        Lekéri az összes chunk embeddinget.
        Később egyszerűen lecserélhető Elasticsearch lekérésre.
        """
        return KnowledgeEmbedding.objects.select_related("chunk").all()

    # ---------------------------------------------------------------------
    def search(
        self,
        query: str,
        top_k: int = None,
        threshold: float = None,
    ) -> List[Tuple[KnowledgeChunk, float]]:
        """
        Embedding alapú keresés a chunkok között.

        Visszatérés:
            List[(chunk_obj, similarity_score)]
        """

        # Alapértelmezett paraméterek
        top_k = top_k or DEFAULT_TOP_K
        threshold = threshold or DEFAULT_SIMILARITY_THRESHOLD

        # ------------------------------------------------------------
        # 1) Query embedding előállítása
        # ------------------------------------------------------------
        query_vector = self._get_query_embedding(query)
        if not query_vector:
            return []

        # ------------------------------------------------------------
        # 2) Összes chunk embedding lekérése
        # ------------------------------------------------------------
        embeddings = self._get_all_embeddings()
        scored_results = []

        # ------------------------------------------------------------
        # 3) Similarity számítás chunkonként
        # ------------------------------------------------------------
        for emb in embeddings:
            try:
                similarity = cosine_similarity(query_vector, emb.vector)
            except Exception:
                similarity = 0.0

            scored_results.append((emb.chunk, similarity))

        # ------------------------------------------------------------
        # 4) Rangsorolás similarity alapján
        # ------------------------------------------------------------
        scored_results.sort(key=lambda x: x[1], reverse=True)

        # ------------------------------------------------------------
        # 5) TOP-K visszaadás
        # ------------------------------------------------------------
        return scored_results[:top_k]
