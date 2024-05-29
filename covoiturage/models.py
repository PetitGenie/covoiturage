from django.db import models
from django.contrib.auth.models import User




class Trajet(models.Model):
    point_depart = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    heure_depart = models.TimeField(editable=True)
    places_disponibles = models.IntegerField()
    date = models.DateField(editable=True, null=True)
    modele = models.CharField(max_length=35, null=True)
    plaque = models.CharField(max_length=10, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False)
   
    def __str__(self):
        return f"{self.point_depart} - {self.destination}"



class Reservation(models.Model):
    STATUT_CHOICES = (
        ('En attente', 'En attente'),
        ('Confiirme', 'Confirme'),
        ('Annule', 'Annule'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    date = models.DateTimeField(editable=True, null=True)
    avance_payee=models.PositiveIntegerField(editable=True, null=True)
    statut= models.CharField(max_length=10, choices=STATUT_CHOICES, default='En attente')

    def annuler_resvation(self):
        if self.statut == 'En attente':
            self.statut = 'annule'
            self.save()
    
    def confirmer_reservation(self):
        if self.statut == 'En attente':
            self.statut = 'confirme'
            self.save()
   
    def __str__(self):
        return f"{self.user} - {self.trajet}"

class Commentaire(models.Model):
    commentaire = models.TextField()
    note = models.IntegerField()
    client = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.commentaire

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contenu = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.contenu


class Paiement(models.Model):
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    montant = models.PositiveIntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user} - {self.montant}"






