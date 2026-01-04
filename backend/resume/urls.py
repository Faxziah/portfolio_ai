from django.urls import path
from . import views

urlpatterns = [
    path("resume/", views.get_resume, name="get-resume"),
    path("resume/carousel/", views.get_carousel, name="get_carousel"),
    path("resume/documents/", views.get_documents, name="get_documents"),
    path("settings/", views.get_settings, name="get_settings"),
    path("translations/", views.get_translations, name="get_translations"),
    path("csrf/", views.get_csrf_token, name="get_csrf_token"),
]

