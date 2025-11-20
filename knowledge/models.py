#file: knowledge/models.py
# Tudásbázis modellek: kategóriák, tudáselemek, chunkok, embeddingek és rendszer beállítások.
# A slug-ok automatikusan generálódnak a save() metódusban.

from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


# -------------------------------------------------------------------------
# Kategória modell – tudáselemek csoportosításához
# -------------------------------------------------------------------------
class KnowledgeCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Kategória"
        verbose_name_plural = "Kategóriák"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Slug automatikus generálása
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while KnowledgeCategory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter:03d}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


# -------------------------------------------------------------------------
# Tudáselem modell – az érdemi tartalmak tárolása
# -------------------------------------------------------------------------
class KnowledgeItem(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)

    # Eredeti tartalom
    content = models.TextField()

    anonymized_content = models.TextField(
        blank=True,
        null=True,
        help_text="Anonimizált (PII-mentesített) tartalom, amelyen a RAG pipeline dolgozik."
    )

    category = models.ForeignKey(
        "KnowledgeCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tudáselem"
        verbose_name_plural = "Tudáselemek"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Slug automatikus generálása
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while KnowledgeItem.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter:03d}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


# -------------------------------------------------------------------------
# CHUNK modell – a tudáselemek darabolt részei
# -------------------------------------------------------------------------
class KnowledgeChunk(models.Model):
    item = models.ForeignKey(
        KnowledgeItem,
        on_delete=models.CASCADE,
        related_name="chunks"
    )

    index = models.PositiveIntegerField(help_text="Chunk sorszáma (0-al kezdődő).")
    content = models.TextField(help_text="A chunk szöveges tartalma.")

    is_embedded = models.BooleanField(
        default=False,
        help_text="Jelzi, hogy a chunk rendelkezik-e már embedding adattal."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tudás-chunk"
        verbose_name_plural = "Tudás-chunkok"
        ordering = ["item", "index"]
        unique_together = ("item", "index")

    def __str__(self):
        return f"{self.item.title} – chunk #{self.index}"


# -------------------------------------------------------------------------
# EMBEDDING modell – minden chunk embeddingje
# -------------------------------------------------------------------------
class KnowledgeEmbedding(models.Model):
    chunk = models.OneToOneField(
        KnowledgeChunk,
        on_delete=models.CASCADE,
        related_name="embedding"
    )

    vector = models.JSONField(
        help_text="Embedding vektor float listaként."
    )

    model_name = models.CharField(
        max_length=200,
        default="text-embedding-3-small",
        help_text="Embedding generálásához használt modell neve."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Embedding"
        verbose_name_plural = "Embeddingek"

    def __str__(self):
        return f"Embedding – chunk #{self.chunk.index} ({self.model_name})"


# -------------------------------------------------------------------------
# Tudásbázis beállítások (singleton)
# -------------------------------------------------------------------------
class KnowledgeSettings(models.Model):
    auto_embedding = models.BooleanField(default=False)
    auto_anon = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Tudásbázis beállítások"
        verbose_name_plural = "Tudásbázis beállítások"

    def __str__(self):
        return "Tudásbázis beállítások"

    def save(self, *args, **kwargs):
        # Singleton enforcement
        if KnowledgeSettings.objects.exists() and not self.pk:
            raise ValidationError("Már létezik egy Tudásbázis beállítás bejegyzés!")
        super().save(*args, **kwargs)
