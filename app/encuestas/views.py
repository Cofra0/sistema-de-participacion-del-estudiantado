from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from encuestas.models import Encuesta


# Renderiza la pagina principal de encuestas.
@login_required
def encuesta_seleccionada(request):
    id_encuesta = request.GET.get("id", "")
    datos_encuesta = Encuesta.objects.get(id=id_encuesta)
    return render(request, "encuesta_seleccionada.html", datos_encuesta)
