# Generated by Django 5.1.6 on 2025-04-09 05:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividad', '0001_initial'),
        ('calificaciones', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calificacion',
            name='actividad',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='calificaciones_directas', to='actividad.actividad'),
        ),
    ]
