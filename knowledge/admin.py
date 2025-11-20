#file: knowledge/admin.py
# Tudásbázis admin: kategóriák, tudáselemek, chunkok, embeddingek és rendszer beállítások.

from django.contrib import admin, messages
from django.db import transaction
from .models import (
    KnowledgeCategory,
    KnowledgeItem,
    KnowledgeChunk,
    KnowledgeEmbedding,
    KnowledgeSettings,
)

# -------------------------------------------------------------------------
# Kategória admin
# -------------------------------------------------------------------------
@admin.register(KnowledgeCategory)
class KnowledgeCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    readonly_fields = ("slug",)
    ordering = ("name",)

    fieldsets = (
        ("Alapadatok", {
            "fields": ("name", "slug", "description")
        }),
    )


# -------------------------------------------------------------------------
# Tudáselem admin – fizika betöltés/törlés ACTIONOK NÉLKÜL
# -------------------------------------------------------------------------
@admin.register(KnowledgeItem)
class KnowledgeItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_active", "slug", "created_at")
    list_filter = ("is_active", "category")
    search_fields = ("title", "content", "anonymized_content")
    readonly_fields = ("slug", "created_at", "updated_at")
    ordering = ("-created_at",)

    # ⚠️ A korábbi fizika betöltés/törlés actionök eltávolítva
    actions = []

    fieldsets = (
        ("Alapadatok", {
            "fields": ("title", "slug", "category", "is_active")
        }),
        ("Eredeti tartalom", {
            "fields": ("content",)
        }),
        ("Anonimizált tartalom", {
            "fields": ("anonymized_content",),
            "classes": ("collapse",)
        }),
        ("Meta adatok", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


# -------------------------------------------------------------------------
# CHUNK admin – csak olvasható (automatikus generálás)
# -------------------------------------------------------------------------
@admin.register(KnowledgeChunk)
class KnowledgeChunkAdmin(admin.ModelAdmin):
    list_display = ("item", "index", "short_preview", "is_embedded", "created_at")
    list_filter = ("item", "is_embedded")
    search_fields = ("content",)
    readonly_fields = ("item", "index", "content", "is_embedded", "created_at")
    ordering = ("item", "index")

    def short_preview(self, obj):
        return (obj.content[:80] + "...") if len(obj.content) > 80 else obj.content

    short_preview.short_description = "Tartalom előnézet"


# -------------------------------------------------------------------------
# EMBEDDING admin – csak megtekintés
# -------------------------------------------------------------------------
@admin.register(KnowledgeEmbedding)
class KnowledgeEmbeddingAdmin(admin.ModelAdmin):
    list_display = ("chunk", "model_name", "created_at")
    readonly_fields = ("chunk", "model_name", "vector", "created_at")
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False  # csak automatikus generálás támogatott


# -------------------------------------------------------------------------
# Tudásbázis beállítások admin – SINGLETON
# -------------------------------------------------------------------------
@admin.register(KnowledgeSettings)
class KnowledgeSettingsAdmin(admin.ModelAdmin):
    list_display = ("auto_embedding", "auto_anon")

    def has_add_permission(self, request):
        return not KnowledgeSettings.objects.exists()

    def changelist_view(self, request, extra_context=None):
        qs = KnowledgeSettings.objects.all()
        if qs.count() == 1:
            obj = qs.first()
            return self.change_view(
                request,
                object_id=str(obj.id),
                extra_context=extra_context
            )
        return super().changelist_view(request, extra_context)
