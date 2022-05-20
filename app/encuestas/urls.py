from django.urls import path
from . import views

app_name = "encuestas"
urlpatterns = [path("", views.main, name="main"), path("encuestas", views.encuestas, name="encuestas")]
