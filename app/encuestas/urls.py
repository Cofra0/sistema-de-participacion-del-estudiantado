from django.urls import path
from . import views

app_name = "encuestas"
urlpatterns = [
    path("", views.main, name="main"),
    path("nueva_encuesta/", views.agregar_encuesta, name="nueva_encuesta"),
    path("val_url/<path:link>", views.get_status_json, name="val_url"),
]
