#file: knowledge/apps.py
from django.apps import AppConfig


class KnowledgeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'knowledge'
    verbose_name = 'Tudásbázis'

    def ready(self):
        import knowledge.signals