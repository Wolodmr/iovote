from django.apps import AppConfig

class ResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'results'

    def ready(self):
        from . import dash_apps  # Ensure this imports your Dash app


