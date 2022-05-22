from django.contrib.auth.decorators import login_required

# from django.http import HttpResponse, HttpResponseRedirect
# from django.template.loader import get_template
from django.shortcuts import render, redirect, reverse
from encuestas.utils import validar_form
from django.http import HttpResponse, JsonResponse
from encuestas import models
from encuestas.models import Encuesta


# from django.contrib.auth import authenticate, login, logout

# Renderiza la pagina principal de encuestas.
@login_required
def main(request):
    return redirect(reverse("encuestas:encuestas"))


@login_required
def agregar_encuesta(request):

    # Información del usuario
    user = request.user
    user_ins = models.Persona.objects.get(user=user)
    puntos_user = user_ins.puntos

    if request.method == "GET":
        valores = {"puntos": puntos_user, "respuestas_necesarias": 1, "hora_termino": "23:59"}
        return render(request, "formulario.html", {"valores": valores, "puntos_disp": puntos_user})

    elif request.method == "POST":
        errores, valores, addattr, res, date_obj = validar_form.validar_formulario(request, puntos_user)

        if len(errores) == 0:

            # Calculo de los puntos para que no sobren
            puntos_totales = int(valores["puntos"]) - int(valores["puntos"]) % int(valores["respuestas_necesarias"])
            puntos_respuesta = puntos_totales // int(valores["respuestas_necesarias"])

            # Se descuentan los puntos del usuario
            user_ins.puntos -= puntos_totales

            # Se crea la nueva encuesta
            encuesta = models.Encuesta(
                nombre=valores["nombre"],
                descripcion=valores["descripcion"],
                creador=user,
                plazo=date_obj,
                puntos_totales=puntos_totales,
                puntos_encuesta=puntos_respuesta,
                link=valores["link_encuesta"],
                hash=valores["codigo_encuesta"],
            )

            # Se guarda la encuesta
            encuesta.save()

            # Se guardan los cambios del usuario
            user_ins.save()

            # Devolver vista principal. con algún mensaje de éxito?
            return HttpResponse("Se guardó la encuesta")
        else:

            info = {"errores": errores, "valores": valores, "addattr": addattr, "puntos_disp": puntos_user}

            return render(request, "formulario.html", info)


def get_status_json(request, link):
    res = validar_form.get_status_url(link)
    return JsonResponse(res)


# Create your views here.

# Vista de la pagina principal
@login_required
def encuestas(request):  # the index view
    encuestasDisponibles = Encuesta.objects.filter(activa=True).order_by("-puntos_encuesta")
    # Se filtran la encuestas disponibles y se ordenan decrecientemente por puntos
    return render(request, "encuestas/index.html", {"encuestasDisponibles": encuestasDisponibles})


# Vista del resumen de encuestas creadas y respondidas por el usuario
@login_required
def mis_encuestas(request):
    return render(request, "encuestas/missing.html", {})


# Vista del formulario para publicar una encuesta
@login_required
def publicar_encuesta(request):
    return render(request, "encuestas/missing.html", {})


# Vista donde la encuesta está incertada
@login_required
def encuesta_prueba(request):
    return render(request, "encuestas/encuesta_prueba.html", {})
