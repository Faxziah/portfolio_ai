from django.urls import path
from . import views

urlpatterns = [
    path("resume/", views.get_resume, name="get-resume"),
    path("settings/", views.get_settings, name="get_settings"),
    path("translations/", views.get_translations, name="get_translations"),
]

