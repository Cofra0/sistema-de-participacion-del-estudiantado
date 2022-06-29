from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect

# from django.template.loader import get_template
from django.shortcuts import render
from encuestas.utils import validar_form
from django.http import JsonResponse
from encuestas import models
from django.contrib import messages
from encuestas.models import Encuesta, Persona, Responde, Entra
from datetime import timedelta
from django.db.models import Sum
from django.core.paginator import Paginator
from math import floor
from django.urls import reverse
from django.utils import timezone
from tzlocal import get_localzone
from django.contrib.auth import logout as custom_logout

local_tz = get_localzone()

# from django.contrib.auth import authenticate, login, logout

PUNTOS_BASE = 1  # Puntos base a entregar por responder la encuesta independientemente de los puntos ofrecidos por el que la publica


# Vista sólamente llamada desde algún acceso a la encuesta, lo que cuenta cuando
# la persona entra a la encuesta, lo que registramos en un objeto
@login_required
def ver_encuesta(request):
    user = request.user
    id_encuesta = int(request.GET["id"])

    encuesta = Encuesta.objects.get(id=id_encuesta)
    entrada_encuesta = Entra(usuario=user, encuesta=encuesta, fecha_entrada=timezone.now())
    entrada_encuesta.save()

    return HttpResponseRedirect(reverse("encuestas:encuesta") + "?id=" + str(id_encuesta))


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
        "puntos_encuesta": encuesta.reward_points,  # encuesta.puntos_encuesta + PUNTOS_BASE,
        "puntos": puntos_user,
    }

    if request.method == "GET":
        return render(request, "encuestas/encuesta_seleccionada.html", datos_encuesta)

    elif request.method == "POST":
        encuesta = Encuesta.objects.get(id=id_encuesta)
        hash = request.POST["hash"]
        if encuesta.creador == request.user:
            messages.error(request, "No puedes responder una encuesta que has creado")
            return HttpResponseRedirect(request.path_info + "?id=" + str(id_encuesta))
        elif str(hash) == str(encuesta.hash) and not Responde.objects.filter(usuario=request.user, encuesta=encuesta).exists():

            # Guardamos los datos de haber respondido
            recompensa = encuesta.reward_points
            fecha = timezone.now()
            responde = Responde(usuario=request.user, encuesta=encuesta, fecha=fecha, puntos=recompensa)  # puntos_encuesta + PUNTOS_BASE

            # Obtenemos el último objeto Entra que fue creado para esta encuesta y este usuario en específico
            entra_encuesta = Entra.objects.filter(usuario=request.user, encuesta=encuesta).order_by("-fecha_entrada")
            print(entra_encuesta)
            entra_encuesta = entra_encuesta[0]

            # Guardamos los dato de haber respondido
            responde = Responde(usuario=request.user, encuesta=encuesta, fecha=fecha, puntos=recompensa, entrada_encuesta=entra_encuesta)
            responde.save()

            # Devolver vista principal. con algún mensaje de éxito?
            messages.success(request, f"Has reclamado {str(recompensa)} puntos")
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

            print(date_obj)

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

    encuestasDisponibles = sorted(Encuesta.objects.filter(activa=True).exclude(creador=request.user), key=lambda t: t.reward_points, reverse=True)
    # encuestasDisponibles = Encuesta.objects.filter(activa=True).order_by(
    #    "-puntos_encuesta"
    # Se filtran la encuestas disponibles y se ordenan decrecientemente por puntos
    # Se realiza el filtro adicional
    for encuesta in encuestasDisponibles:
        encuesta.active

    encuestas = [{**x.__dict__, "reward_points": x.reward_points, "participantes": x.participantes.count()} for x in encuestasDisponibles]

    # Estarán actualizados si se cerró la encuesta
    puntos = Persona.objects.get(user=request.user).puntos

    for i in range(len(encuestas)):
        fecha = encuestasDisponibles[i].plazo - timezone.now()
        fechaSegundos = fecha.seconds
        fechaDias = fecha.days
        hours, remainder = divmod(fechaSegundos, 3600)
        minutes, seconds = divmod(remainder, 60)

        if fecha < timezone.now() - timezone.now():
            encuestas[i]["plazo"] = "00s"
        elif fechaDias != 0:
            encuestas[i]["plazo"] = "{}d".format(int(fechaDias))
        elif int(hours) != 0:
            encuestas[i]["plazo"] = "{:02}:{:02}:{:02}h".format(int(hours), int(minutes), int(seconds))
        elif int(minutes) != 0:
            encuestas[i]["plazo"] = "{:02}:{:02}m".format(int(minutes), int(seconds))
        else:
            encuestas[i]["plazo"] = "{:02}s".format(int(seconds))
        encuestas[i]["puntos_encuesta"] = encuestas[i]["reward_points"]

    paginator = Paginator(encuestas, 15)  # Mostramos 15 encuestas por pagina

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "encuestas/index.html", {"encuestas": encuestas, "puntos": puntos, "page_obj": page_obj})


# Vista del resumen de encuestas creadas y respondidas por el usuario
@login_required
def mis_encuestas(request):
    publicadas = Encuesta.objects.filter(creador=request.user)

    # Asegurarse que las encuestas estén activas
    for encuesta in publicadas:
        encuesta.active

    publicadas = publicadas.order_by("-activa")
    encuestas_publicadas = [{**x.__dict__, "reward_points": x.reward_points, "participantes": x.participantes.count()} for x in publicadas]
    # encuestas_publicadas = list(publicadas.values())

    respondidas = Responde.objects.filter(usuario=request.user).order_by("-puntos")

    puntos = Persona.objects.get(user=request.user).puntos
    puntos_ganados = respondidas.aggregate(Sum("puntos"))
    pg_num = puntos_ganados["puntos__sum"]
    puntos_ganados["puntos__sum"] = pg_num if pg_num is not None else 0
    cantidad_respondidas = respondidas.count()
    cantidad_publicadas = publicadas.count()

    for i in range(len(encuestas_publicadas)):
        fecha = publicadas[i].plazo - timezone.now()
        fechaSegundos = fecha.seconds
        fechaDias = fecha.days
        hours, remainder = divmod(fechaSegundos, 3600)
        minutes, seconds = divmod(remainder, 60)

        if fecha <= timedelta(0) or not encuestas_publicadas[i]["activa"]:
            encuestas_publicadas[i]["plazo"] = "Terminado"
        elif fechaDias != 0:
            encuestas_publicadas[i]["plazo"] = "{}d".format(int(fechaDias))
        elif int(hours) != 0:
            encuestas_publicadas[i]["plazo"] = "{:02}:{:02}:{:02}h".format(int(hours), int(minutes), int(seconds))
        elif int(minutes) != 0:
            encuestas_publicadas[i]["plazo"] = "{:02}:{:02}m".format(int(minutes), int(seconds))
        else:
            encuestas_publicadas[i]["plazo"] = "{:02}s".format(int(seconds))

    return render(
        request,
        "encuestas/mis_encuestas.html",
        {
            "puntos": puntos,
            "puntos_ganados": puntos_ganados,
            "cantidad_publicadas": cantidad_publicadas,
            "cantidad_contestadas": cantidad_respondidas,
            "publicadas": encuestas_publicadas,
            "respondidas": respondidas,
        },
    )


# Vista donde la encuesta está incertada
@login_required
def encuesta_prueba(request):
    puntos = Persona.objects.get(user=request.user).puntos
    return render(request, "encuestas/encuesta_prueba.html", {"puntos": puntos})


@login_required
def modificar_encuesta(request):
    user = request.user
    persona = Persona.objects.get(user=user)
    puntos = persona.puntos
    encuesta = []
    error = False
    if request.method == "GET":
        id_encuesta = int(request.GET.get("id", -1))
    elif request.method == "POST":
        id_encuesta = int(request.POST.get("id", -1))

    # Por si se ponen a jugar con la url
    try:
        encuesta = Encuesta.objects.get(id=id_encuesta, creador=user, activa=True)

        # Actualizar estado por si las moscas, habrá error si la encuesta se desactiva
        error = not encuesta.active

    except Encuesta.DoesNotExist:
        error = True

    # Se abre la página
    if request.method == "GET":
        encuesta.plazo = encuesta.plazo.astimezone(local_tz)
        print(encuesta.plazo)
        return render(request, "encuestas/modificar_encuesta.html", {"puntos": puntos, "error": error, "encuesta": encuesta})

    elif request.method == "POST":
        errores, valores, addattr, res, date_obj = validar_form.validar_actualizacion(request, puntos)

        # No se modifica si hay errores o la encuesta cumplió su plazo al mandar la modificación
        if len(errores) == 0 and encuesta.active:

            # Calculo de los puntos para que no sobren, solamente si la encuesta ya daba más que los puntos base

            if encuesta.puntos_encuesta > 0:
                print(valores["puntos"])
                respuestas_extra = floor(int(valores["puntos"]) / encuesta.puntos_encuesta)
                puntos_extra = respuestas_extra * encuesta.puntos_encuesta
                print(puntos_extra)

            else:
                puntos_extra = 0

            nuevo_total = puntos_extra + encuesta.puntos_totales
            # Se descuentan los puntos del usuario
            persona.puntos -= puntos_extra

            # Se actualiza la encuesta
            encuesta.nombre = valores["nombre"]
            encuesta.puntos_totales = nuevo_total
            encuesta.descripcion = valores["descripcion"]
            encuesta.plazo = date_obj

            encuesta.save()

            # Se guardan los cambios del usuario
            persona.save()

            # Devolver vista principal. con algún mensaje de éxito?
            messages.success(request, "Se guardaron los cambios")
            return HttpResponseRedirect(request.path_info + "?id=" + str(id_encuesta))
        else:

            info = {
                "error": error,
                "errores": errores,
                "valores": valores,
                "addattr": addattr,
                "puntos_disp": puntos,
                "puntos": puntos,
            }

            return render(request, "encuestas/modificar_encuesta.html", info)


@login_required
def cerrar_encuesta(request):
    user = request.user
    if request.method == "GET":
        id_encuesta = int(request.GET.get("id", -1))
        try:
            encuesta = Encuesta.objects.get(id=id_encuesta, creador=user, activa=True)
            encuesta.closing_survey()
        except Encuesta.DoesNotExist:
            return HttpResponseRedirect("/mis_encuestas/")
    return HttpResponseRedirect("/mis_encuestas/")


# Vista de manual de usuario
@login_required
def manual(request):
    puntos = Persona.objects.get(user=request.user).puntos
    return render(request, "encuestas/manual.html", {"puntos": puntos})


# Logout personalizado
@login_required
def cerrar_sesion(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    ip_address = request.META.get("HTTP_X_FORWARDED_FOR", "0xL").split(", ")[0]
    ldata = {"ip_address": ip_address, "username": request.user.username}
    if not username:
        print("intenta logout sin estar logeado", ldata)
    else:
        print("logout usuario", ldata)
    custom_logout(request)
    return HttpResponseRedirect("https://ucampus.uchile.cl/")
