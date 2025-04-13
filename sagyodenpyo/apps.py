from django.apps import AppConfig

class SagyodenpyoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sagyodenpyo'

    def ready(self):
        import sagyodenpyo.signals
