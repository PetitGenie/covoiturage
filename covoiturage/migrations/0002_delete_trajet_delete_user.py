# Generated by Django 5.0.4 on 2024-04-29 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('covoiturage', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Trajet',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]