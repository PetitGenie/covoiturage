# Generated by Django 5.0.4 on 2024-05-02 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covoiturage', '0006_remove_vehicule_annee_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paiement',
            old_name='ref_utilisateur_paiement',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='ref_client_res',
            new_name='client',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='ref_trajet_res',
            new_name='trajet',
        ),
        migrations.RenameField(
            model_name='vehicule',
            old_name='ref_conducteur_vehicule',
            new_name='conducteur_vehicule',
        ),
        migrations.AlterField(
            model_name='paiement',
            name='montant',
            field=models.PositiveIntegerField(),
        ),
        migrations.DeleteModel(
            name='HistoriqueTrajet',
        ),
    ]
