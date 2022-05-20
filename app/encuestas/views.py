from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Renderiza la pagina principal de encuestas.
@login_required
def main(request):
    return render(request, "main.html")
