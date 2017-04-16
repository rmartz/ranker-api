from __future__ import unicode_literals

from django.apps import AppConfig


class CategorizerConfig(AppConfig):
    name = 'categorizer'

    def ready(self):
        from categorizer import signals
