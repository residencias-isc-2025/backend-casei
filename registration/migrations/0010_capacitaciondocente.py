# Generated by Django 5.1.6 on 2025-03-01 22:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_remove_formacionacademica_institucion_pais'),
    ]

    operations = [
        migrations.CreateModel(
            name='CapacitacionDocente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_capacitacion', models.CharField(max_length=255)),
                ('año_obtencion', models.PositiveIntegerField()),
                ('horas', models.PositiveIntegerField()),
                ('institucion_pais', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='capacitaciones', to='registration.institucionpais')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capacitaciones_docentes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
