from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CustomUser(User):
    # Por simplicidad se extiende el usuario de django
    # id -> automatico si no se define primary key

    puntos = models.IntegerField(verbose_name="Puntos disponibles del usuario", default=1)


class Encuesta(models.Model):
    # id -> automatico

    nombre = models.CharField(verbose_name="Nombre de encuesta", max_length=50)

    descripcion = models.CharField(verbose_name="Descripción de la encuesta", max_length=255)

    creador = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="Crea")

    # Para la tabla intermedia
    participantes = models.ManyToManyField(CustomUser, through="Responde", related_name="Participa")

    plazo = models.DateTimeField(verbose_name="Fecha límite para responder")

    puntos_totales = models.IntegerField(
        verbose_name="Puntos disponibles de la encuesta",
    )

    puntos_encuesta = models.IntegerField(verbose_name="Puntos que entrega la encuesta por responder")

    link = models.URLField(verbose_name="Url de la encuesta")

    activa = models.BooleanField(verbose_name="Determina si la encuesta está activa o no", default=True)


class Responde(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

    fecha = models.DateTimeField(verbose_name="Fecha de la respuesta")

    puntos = models.IntegerField(verbose_name="Puntos entregados por responder")
