from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from encuestas import models
from argparse import RawTextHelpFormatter


class Command(BaseCommand):

    help = """
Resta la cantidad de puntos al usuario ingresado (resta la mitad de los puntos por defecto)

Ejemplos:
python manage.py quitar_puntos 1234567 --puntos 50
python manage.py quitar_puntos 1234567
    """

    def create_parser(self, *args, **kwargs):
        parser = super(Command, self).create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def add_arguments(self, parser):

        parser.add_argument("usuario", type=int, help="Rut del usuario sin dígito verificador")
        parser.add_argument("--puntos", type=int, help="Cantidad de puntos a restar")

    def handle(self, *args, **options):

        try:
            usuario = User.objects.get(username=options["usuario"])

            if options["puntos"] and options["puntos"] < 0:

                self.stdout.write(self.style.ERROR("La cantidad de puntos debe ser mayor a 0"))

            else:

                usuario_plataforma = models.Persona.objects.get(user=usuario)

                restar = usuario_plataforma.puntos // 2 + usuario_plataforma.puntos % 2 if options["puntos"] is None else options["puntos"]

                if usuario_plataforma.puntos >= restar:

                    usuario_plataforma.puntos -= restar

                else:

                    usuario_plataforma.puntos = 0

                usuario_plataforma.save()

                self.stdout.write(self.style.SUCCESS(f"Se han quitado los puntos. Quedó con {usuario_plataforma.puntos} puntos"))

        except User.DoesNotExist:

            self.stdout.write(self.style.ERROR("El usuario no existe"))

        except models.Persona.DoesNotExist:

            self.stdout.write(self.style.ERROR("El usuario ingresado no está registrado en la plataforma"))
