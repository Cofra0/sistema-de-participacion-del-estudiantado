from django.urls import path
from . import views

app_name = "encuestas"
urlpatterns = [
    path("encuestas/", views.encuestas, name="encuestas"),
    path("mis_encuestas/", views.mis_encuestas, name="mis_encuestas"),
    path("publicar_encuesta/", views.publicar_encuesta, name="publicar_encuestas"),
    path("encuesta/", views.encuesta, name="encuesta"),
]
