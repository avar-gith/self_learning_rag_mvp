#file: services/rag/rag_service.py
# RAG kereső szolgáltatás – embedding alapú hasonlóság keresés
# Bővítve: kategória-alapú embedding szűrés LLM felismerés alapján.

from typing import List, Tuple
import numpy as np
from django.db.models import QuerySet

from services.embedding.embedding_service import EmbeddingService
from services.ai_provider import get_ai_client
from knowledge.models import KnowledgeEmbedding, KnowledgeChunk, KnowledgeCategory


# -------------------------------------------------------------------------
# Alapértelmezett RAG paraméterek
# -------------------------------------------------------------------------
DEFAULT_TOP_K = 5
DEFAULT_SIMILARITY_THRESHOLD = 0.35


# -------------------------------------------------------------------------
# Koszinusz hasonlóság számítás
# -------------------------------------------------------------------------
def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Két embedding vektor koszinusz hasonlóságát számítja ki."""
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
    Embedding alapú hasonlóság keresés, kategória-alapú szűréssel bővítve.
    """

    def __init__(self, embedding_client=None):
        if embedding_client is None:
            embedding_client = get_ai_client("openai")

        self.embedding_service = EmbeddingService(embedding_client)

    # ---------------------------------------------------------------------
    def _get_query_embedding(self, query: str):
        """Felhasználói kérdés embeddingje."""
        try:
            return self.embedding_service.create_embedding(query)
        except Exception as e:
            print(f"[RAG] Hiba a query embedding generálásakor: {e}")
            return None

    # ---------------------------------------------------------------------
    def _get_embeddings_by_category(self, category_name: str) -> QuerySet:
        """
        Csak az adott kategóriához tartozó embeddingeket adja vissza.
        """
        try:
            category = KnowledgeCategory.objects.get(name=category_name)
        except KnowledgeCategory.DoesNotExist:
            return KnowledgeEmbedding.objects.none()

        return KnowledgeEmbedding.objects.select_related("chunk", "chunk__item") \
            .filter(chunk__item__category=category)

    # ---------------------------------------------------------------------
    def _get_all_embeddings(self) -> QuerySet:
        """Fallback: összes chunk embedding."""
        return KnowledgeEmbedding.objects.select_related("chunk", "chunk__item").all()

    # ---------------------------------------------------------------------
    def search(
        self,
        query: str,
        top_k: int = None,
        threshold: float = None,
        category_name: str = None,
    ) -> List[Tuple[KnowledgeChunk, float]]:
        """
        Embedding alapú keresés chunkok között – kategória-szűrés támogatással.

        Paraméterek:
            query (str): felhasználói kérdés
            top_k (int)
            threshold (float)
            category_name (str): ha megadott, csak a kategória chunkjai között keres

        Visszatér:
            List[(chunk_obj, similarity_score)]
        """

        top_k = top_k or DEFAULT_TOP_K
        threshold = threshold or DEFAULT_SIMILARITY_THRESHOLD

        # ------------------------------------------------------------
        # 1) Query embedding
        # ------------------------------------------------------------
        query_vector = self._get_query_embedding(query)
        if not query_vector:
            return []

        # ------------------------------------------------------------
        # 2) Embeddingek lekérése kategória alapján
        # ------------------------------------------------------------
        if category_name:
            embeddings = self._get_embeddings_by_category(category_name)
        else:
            embeddings = self._get_all_embeddings()

        scored_results = []

        # ------------------------------------------------------------
        # 3) Similarity számítás
        # ------------------------------------------------------------
        for emb in embeddings:
            try:
                similarity = cosine_similarity(query_vector, emb.vector)
            except Exception:
                similarity = 0.0

            scored_results.append((emb.chunk, similarity))

        # ------------------------------------------------------------
        # 4) Rendezés
        # ------------------------------------------------------------
        scored_results.sort(key=lambda x: x[1], reverse=True)

        # ------------------------------------------------------------
        # 5) TOP-K
        # ------------------------------------------------------------
        return scored_results[:top_k]
