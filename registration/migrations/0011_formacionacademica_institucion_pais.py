# Generated by Django 5.1.6 on 2025-03-02 05:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0010_capacitaciondocente'),
    ]

    operations = [
        migrations.AddField(
            model_name='formacionacademica',
            name='institucion_pais',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='formaciones_academicas', to='registration.institucionpais'),
        ),
    ]
