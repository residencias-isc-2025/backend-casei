# Generated by Django 5.1.6 on 2025-04-07 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub_temas', '0001_initial'),
        ('temas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='temas',
            name='sub_temas',
            field=models.ManyToManyField(blank=True, related_name='temas', to='sub_temas.subtema'),
        ),
    ]
