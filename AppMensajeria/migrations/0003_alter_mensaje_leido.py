# Generated by Django 4.1.3 on 2023-01-02 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMensajeria', '0002_mensaje_leido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='leido',
            field=models.BooleanField(default=False),
        ),
    ]
