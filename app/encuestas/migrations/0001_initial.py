# Generated by Django 4.0.4 on 2022-05-20 20:53

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('puntos', models.IntegerField(default=1, verbose_name='Puntos disponibles del usuario')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre de encuesta')),
                ('descripcion', models.CharField(max_length=255, verbose_name='Descripción de la encuesta')),
                ('plazo', models.DateTimeField(verbose_name='Fecha límite para responder')),
                ('puntos_totales', models.IntegerField(verbose_name='Puntos disponibles de la encuesta')),
                ('puntos_encuesta', models.IntegerField(verbose_name='Puntos que entrega la encuesta por responder')),
                ('link', models.URLField(verbose_name='Url de la encuesta')),
                ('activa', models.BooleanField(default=True, verbose_name='Determina si la encuesta está activa o no')),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Crea', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Responde',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(verbose_name='Fecha de la respuesta')),
                ('puntos', models.IntegerField(verbose_name='Puntos entregados por responder')),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuestas.encuesta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntos', models.IntegerField(default=200, verbose_name='Puntos disponibles del usuario')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='encuesta',
            name='participantes',
            field=models.ManyToManyField(related_name='Participa', through='encuestas.Responde', to=settings.AUTH_USER_MODEL),
        ),
    ]
