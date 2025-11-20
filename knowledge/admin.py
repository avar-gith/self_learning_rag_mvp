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
# Admin ACTIONS – Példa tudás betöltése / törlése
# -------------------------------------------------------------------------

@admin.action(description="Példa Fizika tudás betöltése")
def load_sample_physics(modeladmin, request, queryset):
    """
    Betölti a 'Fizika' kategóriát és 10 alap tudáselemet.
    """

    physics_items = [
        ("Newton törvényei", "A klasszikus mechanika három alapvető törvénye..."),
        ("Relativitáselmélet", "Einstein elmélete a téridőről..."),
        ("Fénysebesség", "Vákuumban: 299 792 458 m/s."),
        ("Gravitáció", "Tömegek közötti vonzóerő."),
        ("Kvantummechanika", "A részecskék kvantumos viselkedését írja le."),
        ("Fekete lyukak", "Gravitációs anomáliák, ahonnan a fény sem tud kijutni."),
        ("Atommodellek", "Bohr-modell, kvantummechanikai modell stb."),
        ("Foton", "Az elektromágneses sugárzás kvantuma."),
        ("Hullám-részecske kettősség", "Részek egyszerre hullám és részecske."),
        ("Standard Modell", "A részecskefizika jelenlegi elméleti keretrendszere."),
    ]

    try:
        with transaction.atomic():

            category, _ = KnowledgeCategory.objects.get_or_create(
                name="Fizika",
                defaults={"description": "Alap fizikai jelenségek és fogalmak."}
            )

            created_count = 0

            for title, content in physics_items:
                obj, was_created = KnowledgeItem.objects.get_or_create(
                    title=title,
                    defaults={
                        "content": content,
                        "category": category,
                        "is_active": True,
                    }
                )
                if was_created:
                    created_count += 1

        messages.success(
            request,
            f"✔ Példa fizika tudás betöltve ({created_count} új elem)."
        )

    except Exception as e:
        messages.error(request, f"❌ Hiba történt: {e}")


@admin.action(description="Példa Fizika tudás törlése")
def delete_sample_physics(modeladmin, request, queryset):
    """
    Törli a 'Fizika' kategóriát és minden hozzá tartozó elemet.
    """

    try:
        with transaction.atomic():

            category = KnowledgeCategory.objects.filter(name="Fizika").first()

            if category:
                deleted_items = KnowledgeItem.objects.filter(category=category).count()
                KnowledgeItem.objects.filter(category=category).delete()
                category.delete()

                messages.success(
                    request,
                    f"✔ Fizika kategória és {deleted_items} tudáselem törölve."
                )
            else:
                messages.info(request, "ℹ Nincs 'Fizika' kategória, nincs mit törölni.")

    except Exception as e:
        messages.error(request, f"❌ Hiba történt: {e}")


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
# Tudáselem admin
# -------------------------------------------------------------------------
@admin.register(KnowledgeItem)
class KnowledgeItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_active", "slug", "created_at")
    list_filter = ("is_active", "category")
    search_fields = ("title", "content", "anonymized_content")
    readonly_fields = ("slug", "created_at", "updated_at")
    ordering = ("-created_at",)

    actions = [load_sample_physics, delete_sample_physics]

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
