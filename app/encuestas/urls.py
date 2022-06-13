from django.urls import path
from . import views

app_name = "encuestas"
urlpatterns = [
    path("", views.encuestas, name="encuestas"),
    path("publicar_encuesta/", views.agregar_encuesta, name="nueva_encuesta"),
    path("val_url/<path:link>", views.get_status_json, name="val_url"),
    path("encuestas/", views.encuestas, name="encuestas"),
    path("mis_encuestas/", views.mis_encuestas, name="mis_encuestas"),
    path("encuesta_prueba/", views.encuesta_prueba, name="encuesta"),
    path("encuesta/", views.encuesta_seleccionada, name="encuesta_seleccionada"),
    path("manual/", views.manual, name="manual"),
    path("ver_encuesta/", views.ver_encuesta, name="ver_encuesta"),
]
