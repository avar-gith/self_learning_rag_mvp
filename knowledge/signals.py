#file: knowledge/signals.py
# Signalok a tudáselemek automatikus anonimizálásához, chunkolásához és embeddingeléséhez.

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from knowledge.models import KnowledgeItem, KnowledgeChunk, KnowledgeEmbedding
from services.anonymization.anonymizer_service import TextAnonymizerService
from services.chunking.chunk_service import chunk_text
from services.embedding.embedding_service import EmbeddingService
from services.ai_provider import get_ai_client


# -------------------------------------------------------------------------
# Tudáselem anonimizálása mentés előtt
# -------------------------------------------------------------------------
@receiver(pre_save, sender=KnowledgeItem)
def anonymize_knowledge_item_content(sender, instance, **kwargs):
    """
    A tudáselem eredeti tartalmát anonimizáljuk mentés előtt,
    majd az eredményt az anonymized_content mezőben tároljuk.
    """

    if not instance.content:
        return

    anonymizer = TextAnonymizerService()
    cleaned_text = anonymizer.anonymize_text(instance.content)
    instance.anonymized_content = cleaned_text


# -------------------------------------------------------------------------
# Tudáselem chunkolása mentés után
# -------------------------------------------------------------------------
@receiver(post_save, sender=KnowledgeItem)
def chunk_knowledge_item(sender, instance, created, **kwargs):
    """
    A tudáselem anonimizált tartalmából automatikusan chunkokat készítünk.
    - Először töröljük a régi chunkokat
    - Majd új chunkokat generálunk
    """

    if not instance.anonymized_content:
        return

    # Régi chunkok törlése
    instance.chunks.all().delete()

    chunks = chunk_text(instance.anonymized_content, max_chars=400)

    for idx, chunk_text_value in enumerate(chunks):
        KnowledgeChunk.objects.create(
            item=instance,
            index=idx,
            content=chunk_text_value,
            is_embedded=False
        )


# -------------------------------------------------------------------------
# Automatikus embedding generálás a chunkokhoz
# -------------------------------------------------------------------------
@receiver(post_save, sender=KnowledgeItem)
def embed_knowledge_chunks(sender, instance, created, **kwargs):
    """
    A tudáselemhez tartozó chunkok automatikus beágyazása.
    Minden olyan chunkra fut, amely még nincs embeddingelve.
    ÉLES RENDSZEREKBEN AJÁNLOTT HÁTTÉRFELADAKÉNT KEZELNI.
    """

    # AI provider kiválasztása (.env / settings alapján)
    try:
        client = get_ai_client("openai")  # <-- később adminból is választható lehet
    except Exception as e:
        print(f"❌ LLM provider inicializálása sikertelen: {e}")
        return

    embedding_service = EmbeddingService(client)

    # Minden olyan chunk, ami nincs embedelve
    chunks_to_process = instance.chunks.filter(is_embedded=False)

    for chunk in chunks_to_process:
        vector = embedding_service.create_embedding(chunk.content)

        if vector is None:
            print(f"❌ Nem sikerült embeddinget generálni: chunk #{chunk.index}")
            continue

        # Embedding rekord mentése
        KnowledgeEmbedding.objects.create(
            chunk=chunk,
            vector=vector,
            model_name=client.embedding_model
        )

        # Chunk státusz frissítése
        chunk.is_embedded = True
        chunk.save(update_fields=["is_embedded"])
