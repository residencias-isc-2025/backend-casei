# Generated by Django 5.1.6 on 2025-05-20 03:35

import actividad.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividad', '0002_initial'),
        ('alumno', '0002_alumno_is_active_alter_alumno_apellido_materno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actividad',
            name='alumno_alto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actividades_alto', to='alumno.alumno'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='alumno_alto_calificacion',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='alumno_alto_evidencia',
            field=models.FileField(blank=True, null=True, upload_to=actividad.models.evidencia_path),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='alumno_bajo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actividades_bajo', to='alumno.alumno'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='alumno_bajo_calificacion',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='alumno_bajo_evidencia',
            field=models.FileField(blank=True, null=True, upload_to=actividad.models.evidencia_path),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='alumno_promedio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actividades_promedio', to='alumno.alumno'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='alumno_promedio_calificacion',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='alumno_promedio_evidencia',
            field=models.FileField(blank=True, null=True, upload_to=actividad.models.evidencia_path),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='descripcion',
            field=models.FileField(blank=True, null=True, upload_to='actividades/descripcion/'),
        ),
        migrations.AlterField(
            model_name='actividad',
            name='formato',
            field=models.FileField(blank=True, null=True, upload_to=actividad.models.formato_path),
        ),
    ]
