from django.shortcuts import render

# Create your views here.

# Renderiza la pagina principal de encuestas.
def main(request):
    return render(request, "main.html")