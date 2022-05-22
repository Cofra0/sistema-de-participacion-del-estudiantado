from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from encuestas.utils import validar_form
from django.http import HttpResponse, JsonResponse
from encuestas import models
from encuestas.models import Encuesta


# Renderiza la pagina principal de encuestas.
@login_required
def main(request):
    return render(request, "main.html")


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
def encuesta_seleccionada(request):
    id_encuesta = request.GET.get("id", "")
    datos_encuesta = Encuesta.objects.get(id=id_encuesta)
    return render(request, "encuesta_seleccionada.html", datos_encuesta)
