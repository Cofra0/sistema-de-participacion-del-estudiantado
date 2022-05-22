from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from encuestas.models import Encuesta, Responde
from datetime import datetime
from django.contrib import messages


# Renderiza la pagina principal de encuestas.
@login_required
def encuesta_seleccionada(request):
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
        "puntos_encuesta": encuesta.puntos_encuesta,
    }

    if request.method == "GET":

        return render(request, "encuesta_seleccionada.html", datos_encuesta)

    elif request.method == "POST":
        encuesta = Encuesta.objects.get(id=id_encuesta)
        hash = request.POST["hash"]

        if str(hash) == str(encuesta.hash) and Responde.objects.filter(usuario=request.user, encuesta=encuesta) == []:
            puntos = encuesta.puntos_encuesta
            encuesta.puntos_totales -= puntos
            encuesta.save()
            fecha = datetime.now().strftime("%Y/%m/%d")

            # Guardamos los dato de haber respondido
            responde = Responde(usuario=request.user, encuesta=encuesta, fecha=fecha, puntos=puntos)
            responde.save()

            # Devolver vista principal. con algún mensaje de éxito?
            messages.success(request, f"Has reclamado {str(puntos)} puntos")
            return render(request, "encuesta_seleccionada.html", datos_encuesta)

        elif str(hash) == str(encuesta.hash) and Responde.objects.filter(usuario=request.user, encuesta=encuesta) != []:
            # Devolver vista principal con algún mensaje de que ya reclamo los puntos
            messages.error(request, "Ya has reclamado estos puntos")
            return render(request, "encuesta_seleccionada.html", datos_encuesta)
        else:
            messages.error(request, "Hash incorrecto")
            return render(request, "encuesta_seleccionada.html", datos_encuesta)
