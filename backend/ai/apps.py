from django.apps import AppConfig


class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai'

    def ready(self):
        from django.contrib import admin
        admin.site.site_url = "http://localhost:3000"
