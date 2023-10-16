from django.apps import AppConfig
from .jobs import updater

class DailyreadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dailyreads'

    def ready(self):
        updater.start()
