#file: core/apps.py

from django.apps import AppConfig

class CoreConfig(AppConfig):
    name = 'core'

    # Inicializáláskor betöltjük a signalokat
    def ready(self):
        import core.signals  # noqa
