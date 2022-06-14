import datetime
import re
import urllib.request
from django.conf import settings
import requests
import pytz
from tzlocal import get_localzone

local_tz = get_localzone()


# Utilidad que convierte una fecha string a la misma fecha pasada desde tiempo local a utc
# para ser guardada en la base de datos, cumpliendo con el estandar de guardar los
# objetos de tiempo en utc y sólo convertir a tiempo local en la vista del usuario
def stringToUtc(string):
    date_obj = datetime.datetime.strptime(string, "%Y-%m-%d %H:%M")
    local_datetime = date_obj.replace(tzinfo=local_tz)
    return local_datetime.astimezone(pytz.utc)


def get_status_url(url):
    try:
        if url.find("//") == -1:
            url = url[:6] + "/" + url[6:]
        res = urllib.request.urlopen(url)
        status = res.getcode()
        url = res.url
    except Exception:
        status = 0
        url = ""
    res = {"status": status, "url": url}
    return res


# Se usan las mismas validaciones, se pueden separar en pequeñas funciones para modularidad y código más ordenado.
# No se hace ahora por falta de tiempo uwu


def validar_actualizacion(request, puntos_disp):
    nombre = request.POST["nombre"]
    descripcion = request.POST["descripcion"]
    puntos = request.POST["puntos"]
    fecha_termino = request.POST["fecha-termino"]
    hora_termino = request.POST["hora-termino"]

    errores = {}
    valores = {
        "nombre": nombre,
        "descripcion": descripcion,
        "puntos": puntos,
        "fecha_termino": fecha_termino,
        "hora_termino": hora_termino,
    }
    addattr = {}

    if nombre == "":
        errores["nombre"] = "Se debe ingresar un nombre para la encuesta."
        addattr["nombre"] = "is-invalid"
    elif not (5 <= len(nombre) <= 50):
        errores["nombre"] = "El nombre debe tener entre 5 y 50 caracteres."
        addattr["nombre"] = "is-invalid"

    if descripcion == "":
        errores["descripcion"] = "Se debe ingresar una descripción para la encuesta."
        addattr["descripcion"] = "is-invalid"
    elif not (5 <= len(descripcion) <= 255):
        errores["descripcion"] = "La descripción de la encuesta debe tener entre 5 y 255 caracteres."
        addattr["descripcion"] = "is-invalid"

    if puntos == "" or not puntos.isdigit() or int(puntos) < 0:
        errores["puntos"] = "Se debe ingresar un número entero positivo."
        addattr["puntos"] = "is-invalid"
    elif int(puntos) > puntos_disp:
        errores["puntos"] = "Puntos superan el máximo disponible."
        addattr["puntos"] = "is-invalid"

    termino = None
    today = datetime.datetime.today().date()

    if fecha_termino == "":
        errores["fecha_termino"] = "Se debe ingresar la fecha de término de la encuesta."
        addattr["fecha_termino"] = "is-invalid"
    else:
        try:
            end_date = datetime.datetime.strptime(fecha_termino, "%Y-%m-%d").date()
            termino = end_date
            if end_date < today:
                errores["fecha_termino"] = "La fecha de término no puede ser anterior a hoy."
                addattr["fecha_termino"] = "is-invalid"
        except Exception:
            errores["fecha_termino"] = "La fecha ingresada no tiene el formato correcto."
            addattr["fecha_termino"] = "is-invalid"

    if hora_termino == "":
        hora_termino = "23:59"
        valores["hora_termino"] = hora_termino
    elif termino and termino == today:
        try:
            end_time = datetime.datetime.strptime(hora_termino, "%H:%M").strftime("%H:%M")
            current_time = datetime.datetime.today().strftime("%H:%M")
            if end_time < current_time:
                errores["hora_termino"] = "La hora de término no puede ser anterior a ahora."
                addattr["hora_termino"] = "is-invalid"
        except Exception:
            errores["hora_termino"] = "La hora ingresada no tiene el formato correcto."
            addattr["hora_termino"] = "is-invalid"

    date_obj = None
    if not errores.get("fecha_termino") and not errores.get("hora_termino"):
        date_obj = stringToUtc(fecha_termino + " " + hora_termino)
    res = {}
    return errores, valores, addattr, res, date_obj


def validar_formulario(request, puntos_disp):

    nombre = request.POST["nombre"]
    descripcion = request.POST["descripcion"]
    puntos = request.POST["puntos"]
    num_resp = request.POST["respuestas-necesarias"]
    fecha_termino = request.POST["fecha-termino"]
    hora_termino = request.POST["hora-termino"]
    num_preg = request.POST["numero-preguntas"]
    link_encuesta = request.POST["link-encuesta"]
    codigo_encuesta = request.POST["codigo-encuesta"]
    recaptcha = grecaptcha_verify(request)

    errores = {}
    valores = {
        "nombre": nombre,
        "descripcion": descripcion,
        "puntos": puntos,
        "respuestas_necesarias": num_resp,
        "fecha_termino": fecha_termino,
        "hora_termino": hora_termino,
        "numero_preguntas": num_preg,
        "link_encuesta": link_encuesta,
        "codigo_encuesta": codigo_encuesta,
        "recaptcha": recaptcha,
    }
    addattr = {}

    if nombre == "":
        errores["nombre"] = "Se debe ingresar un nombre para la encuesta."
        addattr["nombre"] = "is-invalid"
    elif not (5 <= len(nombre) <= 50):
        errores["nombre"] = "El nombre debe tener entre 5 y 50 caracteres."
        addattr["nombre"] = "is-invalid"

    if descripcion == "":
        errores["descripcion"] = "Se debe ingresar una descripción para la encuesta."
        addattr["descripcion"] = "is-invalid"
    elif not (5 <= len(descripcion) <= 255):
        errores["descripcion"] = "La descripción de la encuesta debe tener entre 5 y 255 caracteres."
        addattr["descripcion"] = "is-invalid"

    if puntos == "" or not puntos.isdigit() or int(puntos) < 0:
        errores["puntos"] = "Se debe ingresar un número entero positivo."
        addattr["puntos"] = "is-invalid"
    elif int(puntos) > puntos_disp:
        errores["puntos"] = "Puntos superan el máximo disponible."
        addattr["puntos"] = "is-invalid"

    if num_resp == "" or not num_resp.isdigit() or int(num_resp) < 0:
        errores["respuestas_necesarias"] = "Se debe ingresar un número entero positivo."
        addattr["respuesta_necesarias"] = "is-invalid"

    termino = None
    today = datetime.datetime.today().date()

    if fecha_termino == "":
        errores["fecha_termino"] = "Se debe ingresar la fecha de término de la encuesta."
        addattr["fecha_termino"] = "is-invalid"
    else:
        try:
            end_date = datetime.datetime.strptime(fecha_termino, "%Y-%m-%d").date()
            termino = end_date
            if end_date < today:
                errores["fecha_termino"] = "La fecha de término no puede ser anterior a hoy."
                addattr["fecha_termino"] = "is-invalid"
        except Exception:
            errores["fecha_termino"] = "La fecha ingresada no tiene el formato correcto."
            addattr["fecha_termino"] = "is-invalid"

    if hora_termino == "":
        hora_termino = "23:59"
        valores["hora_termino"] = hora_termino
    elif termino and termino == today:
        try:
            end_time = datetime.datetime.strptime(hora_termino, "%H:%M").strftime("%H:%M")
            current_time = datetime.datetime.today().strftime("%H:%M")
            if end_time < current_time:
                errores["hora_termino"] = "La hora de término no puede ser anterior a ahora."
                addattr["hora_termino"] = "is-invalid"
        except Exception:
            errores["hora_termino"] = "La hora ingresada no tiene el formato correcto."
            addattr["hora_termino"] = "is-invalid"

    date_obj = None
    if not errores.get("fecha_termino") and not errores.get("hora_termino"):
        date_obj = stringToUtc(fecha_termino + " " + hora_termino)

    if num_preg == "" or not num_preg.isdigit() or int(num_preg) < 0:
        errores["numero_preguntas"] = "Se debe ingresar un número entero positivo."
        addattr["numero_preguntas"] = "is-invalid"

    res = {}

    if link_encuesta == "":
        errores["link_encuesta"] = "Se debe ingresar el enlace a la encuesta de Google Forms."
        addattr["link_encuesta"] = "is-invalid"
    else:
        shortUrl = r"https:\/\/forms.gle\/([\w-]){17}"
        longUrl = r"https:\/\/docs.google.com\/forms\/d\/e\/[\w-]{56}\/viewform(\?usp=sf_link)?"
        if not re.fullmatch(shortUrl, link_encuesta) and not re.fullmatch(longUrl, link_encuesta):
            errores["link_encuesta"] = "El enlace no corresponde a un Google Form."
            addattr["link_encuesta"] = "is-invalid"
        else:
            res = get_status_url(link_encuesta)
            if res["status"] != 200:
                errores["link_encuesta"] = "No corresponde a una encuesta válida."
                addattr["link_encuesta"] = "is-invalid"

    if codigo_encuesta == "":
        errores["codigo_encuesta"] = "Se debe ingresar el código de verificación de respuesta."
        addattr["codigo_encuesta"] = "is-invalid"
    elif len(codigo_encuesta) > 255:
        errores["codigo_encuesta"] = "No puede tener más de 255 caracteres."
        addattr["codigo_encuesta"] = "is-invalid"

    if not recaptcha["status"]:
        errores["recaptcha"] = "Se debe contestar el Captcha"
        addattr["recaptcha"] = "is-invalid"

    return errores, valores, addattr, res, date_obj


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def grecaptcha_verify(request):
    if request.method == "POST":
        response = {}
        data = request.POST
        captcha_rs = data.get("g-recaptcha-response")
        url = "https://www.google.com/recaptcha/api/siteverify"
        params = {"secret": settings.RECAPTCHA_PRIVATE_KEY, "response": captcha_rs, "remoteip": get_client_ip(request)}
        verify_rs = requests.get(url, params=params, verify=True)
        verify_rs = verify_rs.json()
        response["status"] = verify_rs.get("success", False)
        response["message"] = verify_rs.get("error-codes", None) or "Unspecified error."
        return response
