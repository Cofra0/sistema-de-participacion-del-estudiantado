from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    puntos = models.IntegerField(verbose_name="Puntos disponibles del usuario", default=200)


# class CustomUser(User):
# Por simplicidad se extiende el usuario de django
# id -> automatico si no se define primary key

#    puntos = models.IntegerField(verbose_name="Puntos disponibles del usuario", default=1)


class Encuesta(models.Model):
    # id -> automatico

    nombre = models.CharField(verbose_name="Nombre de encuesta", max_length=50)

    descripcion = models.CharField(verbose_name="Descripción de la encuesta", max_length=255)

    creador = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="Crea")

    # Para la tabla intermedia
    participantes = models.ManyToManyField(User, through="Responde", related_name="Participa")

    plazo = models.DateTimeField(verbose_name="Fecha límite para responder")

    puntos_totales = models.IntegerField(
        verbose_name="Puntos disponibles de la encuesta",
    )

    puntos_encuesta = models.IntegerField(verbose_name="Puntos que entrega la encuesta por responder")

    link = models.URLField(verbose_name="Url de la encuesta")

    activa = models.BooleanField(verbose_name="Determina si la encuesta está activa o no", default=True)

    hash = models.CharField(
        verbose_name="Código para reclamar puntos de encuesta (Máximo de 200 carácteres)",
        max_length=255,
        default="Paral3l3pipedo",  # Hash por defecto (De otra forma no me dejaba hacer la migración uwu)
    )

    @property
    def active(self):
        """
        Propiedad para saber si una encuesta está activa, si ha pasado el plazo entonces retornará False
        y se actualizará la base de datos.
        De otra forma se retornará el campo "activa" de la BBDD.
        """
        # Primero cachar si hay plazo
        if self.plazo < datetime.now():
            # No hay plazo, se cierra la encuesta.
            self.closing_survey()
            return False
        # El plazo no ha acabado, se retorna el valor de "activa" (si la encuesta fue eliminada será false)
        return self.activa

    def closing_survey(self):
        """
        Llamar cuando se elimine una encuesta o se termine el plazo.
        Devuelve los puntos restantes de la encuesta al creador de esta y deja el campo "activa" en False.
        """
        # Si la encuesta aún tiene puntos asignados
        if self.puntos_totales > 0:
            creador = self.creador.persona
            creador.puntos += self.puntos_totales  # Se le retornan los puntos al creador
            self.puntos_totales = 0  # Se quitan los puntos a la encuesta

            # Se guardan los cambios
            creador.save()
        self.puntos_encuesta = 0  # Por si las moscas, la encuesta ya no debería poder repartir puntos
        self.activa = False  # Se cierra la encuesta
        self.save()


class Responde(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

    fecha = models.DateTimeField(verbose_name="Fecha de la respuesta")

    puntos = models.IntegerField(verbose_name="Puntos entregados por responder")


# Para que se cree una persona cada vez que se crea un usuario
@receiver(post_save, sender=User)
def handler(sender, instance, created, **kwargs):
    if created:
        Persona.objects.create(user=instance)

@receiver(post_save, sender=Responde)
def givePoints(sender, answer, created, **kwargs):
    """
    Método que se ejecuta al momento de guardar una respuesta de encuestas. Aquí se agregan
    los puntos correspondientes al usuario simplemente.
    El enviador de la señal es Responde, y se obtiene la instancia creada de Respuesta
    """
    if created:
        user = answer.usuario
        user_points = user.puntos
        setattr(user, "puntos", user_points + answer.puntos)
        user.save()  # guardamos los cambios

def setBasePoints(survey, base_points):
    """
    Método que establece la cantidad de puntos a la cantidad base
    """
    setattr(survey, "puntos_encuesta", base_points)
    survey.save()

@receiver(post_save, sender=Responde)
def discountSurveyPoints(sender, answer, created, **kwargs):
    survey = answer.encuesta
    actual_survey_points = answer.puntos_totales
    if created and actual_survey_points != 0: #Verificamos que no se hayan acabado los puntos de la encuesta
        points_to_discount = answer.puntos_encuesta
        new_points = actual_survey_points - points_to_discount
        if (new_points == 0): # Se acabaron los puntos y debemos setearlo a lo base
            setBasePoints(survey, 1) # Por ahora los puntos base son 10 puntos
        setattr(survey, "puntos_totales", new_points)
        survey.save()
