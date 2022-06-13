# Generated by Django 4.0.5 on 2022-06-12 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("encuestas", "0003_encuesta_hash"),
    ]

    operations = [
        migrations.CreateModel(
            name="Entra",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("fecha_entrada", models.DateTimeField(verbose_name="Fecha de la entrada")),
                ("encuesta", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="encuestas.encuesta")),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name="responde",
            name="entrada_encuesta",
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to="encuestas.entra"),
            preserve_default=False,
        ),
    ]
