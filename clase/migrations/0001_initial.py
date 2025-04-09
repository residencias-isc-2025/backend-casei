# Generated by Django 5.1.6 on 2025-04-09 03:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alumno', '0001_initial'),
        ('carrera', '0001_initial'),
        ('materias', '0001_initial'),
        ('periodo', '0003_periodo_clave'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.CharField(choices=[('01', 'Grupo 01'), ('02', 'Grupo 02'), ('03', 'Grupo 03')], max_length=2)),
                ('alumnos', models.ManyToManyField(related_name='clases', to='alumno.alumno')),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clases', to='carrera.carrera')),
                ('materia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clases', to='materias.materia')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clases', to='periodo.periodo')),
            ],
        ),
    ]
