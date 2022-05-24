from django.contrib.auth.decorators import login_required

# from django.http import HttpResponse, HttpResponseRedirect
# from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.shortcuts import render
from encuestas.utils import validar_form
from django.http import JsonResponse
from encuestas import models
from django.contrib import messages
from encuestas.models import Encuesta, Persona, Responde
from datetime import datetime, timezone
from django.core.paginator import Paginator


# from django.contrib.auth import authenticate, login, logout

PUNTOS_BASE = 1  # Puntos base a entregar por responder la encuesta independientemente de los puntos ofrecidos por el que la publica


# Renderiza la pagina principal de encuestas.
@login_required
def encuesta_seleccionada(request):
    user = request.user
    user_ins = models.Persona.objects.get(user=user)
    puntos_user = user_ins.puntos

    id_encuesta = int(request.GET["id"])
    encuesta = Encuesta.objects.get(id=id_encuesta)

    link = encuesta.link

    if link.endswith("usp=sf_link"):
        link.replace("usp=sf_link", "embedded=true")

    datos_encuesta = {
        "id": id_encuesta,
        "nombre": encuesta.nombre,
        "descripcion": encuesta.descripcion,
        "link": link,
        "puntos_encuesta": encuesta.puntos_encuesta + PUNTOS_BASE,
        "puntos": puntos_user,
    }

    if request.method == "GET":
        return render(request, "encuestas/encuesta_seleccionada.html", datos_encuesta)

    elif request.method == "POST":
        encuesta = Encuesta.objects.get(id=id_encuesta)
        hash = request.POST["hash"]

        if str(hash) == str(encuesta.hash) and not Responde.objects.filter(usuario=request.user, encuesta=encuesta).exists():
            puntos_encuesta = encuesta.puntos_encuesta
            fecha = datetime.now().strftime("%Y-%m-%d")

            # Guardamos los dato de haber respondido
            responde = Responde(usuario=request.user, encuesta=encuesta, fecha=fecha, puntos=puntos_encuesta + PUNTOS_BASE)
            responde.save()

            # Devolver vista principal. con algún mensaje de éxito?
            messages.success(request, f"Has reclamado {str(puntos_encuesta + PUNTOS_BASE)} puntos")
            return HttpResponseRedirect(request.path_info + "?id=" + str(id_encuesta))

        elif str(hash) == str(encuesta.hash) and Responde.objects.filter(usuario=request.user, encuesta=encuesta).exists():
            # Devolver vista principal con algún mensaje de que ya reclamo los puntos
            messages.error(request, "Ya has reclamado estos puntos")
            return HttpResponseRedirect(request.path_info + "?id=" + str(id_encuesta))

        else:
            messages.error(request, "Hash incorrecto")
            return HttpResponseRedirect(request.path_info + "?id=" + str(id_encuesta))


# Vista del formulario para publicar una encuesta
@login_required
def agregar_encuesta(request):

    # Información del usuario
    user = request.user
    user_ins = models.Persona.objects.get(user=user)
    puntos_user = user_ins.puntos

    if request.method == "GET":
        valores = {"puntos": puntos_user, "respuestas_necesarias": 1, "hora_termino": "23:59"}
        return render(
            request,
            "encuestas/formulario.html",
            {"valores": valores, "puntos_disp": puntos_user, "puntos": puntos_user, "puntos_base": PUNTOS_BASE},
        )

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
            messages.success(request, "Se guardó la encuesta")
            return HttpResponseRedirect(request.path_info)
        else:

            info = {
                "errores": errores,
                "valores": valores,
                "addattr": addattr,
                "puntos_disp": puntos_user,
                "puntos": puntos_user,
                "puntos_base": PUNTOS_BASE,
            }

            return render(request, "encuestas/formulario.html", info)


def get_status_json(request, link):
    res = validar_form.get_status_url(link)
    return JsonResponse(res)


# Create your views here.
# Vista de la pagina principal
@login_required
def encuestas(request):  # the index view

    encuestasDisponibles = Encuesta.objects.filter(activa=True).order_by(
        "-puntos_encuesta"
    )  # Se filtran la encuestas disponibles y se ordenan decrecientemente por puntos

    # Se realiza el filtro adicional
    for encuesta in encuestasDisponibles:
        encuesta.active

    # Se vuelve a hacer la query
    encuestasDisponibles = Encuesta.objects.filter(activa=True).order_by("-puntos_encuesta")
    encuestas = list(encuestasDisponibles.values())

    # Estarán actualizados si se cerró la encuesta
    puntos = Persona.objects.get(user=request.user).puntos

    for i in range(len(encuestas)):
        encuestas[i]["plazo"] = (
            encuestasDisponibles[i].plazo - datetime.now(timezone.utc)
        ).days  # se muestran los días faltantes para que termine la encuesta
        encuestas[i]["participantes"] = encuestasDisponibles[
            i
        ].participantes.count()  # se cuentan los usuarios que han participado de la encuesta
        encuestas[i]["puntos_encuesta"] = encuestasDisponibles[i].puntos_encuesta + PUNTOS_BASE

    paginator = Paginator(encuestas, 15)  # Mostramos 15 encuestas por pagina

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "encuestas/index.html", {"encuestas": encuestas, "puntos": puntos, "page_obj": page_obj})


# Vista del resumen de encuestas creadas y respondidas por el usuario
@login_required
def mis_encuestas(request):
    puntos = Persona.objects.get(user=request.user).puntos
    return render(request, "encuestas/missing.html", {"puntos": puntos})


# Vista donde la encuesta está incertada
@login_required
def encuesta_prueba(request):
    puntos = Persona.objects.get(user=request.user).puntos
    return render(request, "encuestas/encuesta_prueba.html", {"puntos": puntos})
