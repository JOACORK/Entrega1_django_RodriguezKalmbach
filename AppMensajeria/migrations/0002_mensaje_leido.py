# Generated by Django 4.1.3 on 2023-01-02 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMensajeria', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='leido',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
