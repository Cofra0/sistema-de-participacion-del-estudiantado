from django.contrib.auth.decorators import login_required

# from django.http import HttpResponse, HttpResponseRedirect
# from django.template.loader import get_template
from django.shortcuts import render
from encuestas.models import Encuesta


# from django.contrib.auth import authenticate, login, logout

# Renderiza la pagina principal de encuestas.
@login_required
def main(request):
    return render(request, "main.html")


# Create your views here.

# Vista de la pagina principal
def encuestas(request):  # the index view
    encuestasDisponibles = Encuesta.objects.filter(activa=True).order_by(
        "-puntos_encuesta"
    )  # Se filtran la encuestas disponibles y se ordenan decrecientemente por puntos
    return render(request, "encuestas/index.html", {"encuestas": encuestasDisponibles})


# Vista del resumen de encuestas creadas y respondidas por el usuario
def mis_encuestas(request):
    return render(request, "encuestas/missing.html", {})


# Vista del formulario para publicar una encuesta
def publicar_encuesta(request):
    return render(request, "encuestas/missing.html", {})


# Vista donde la encuesta está incertada
def encuesta(request):
    return render(request, "encuestas/encuesta.html", {})
