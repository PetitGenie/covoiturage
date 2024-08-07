from django.db import models
from django.contrib.auth.models import User


class Vehicule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicle', null=True)
    modele = models.CharField(max_length=35, null=True)
    plaque = models.CharField(max_length=10, null=True)
    color = models.CharField(max_length=40, null=True)

    def __str__(self):
        return f"{self.modele} - {self.plaque} - {self.color}"

class Trajet(models.Model):
    point_depart = models.CharField(max_length=255)
    passe_par = models.CharField(max_length=255,null=True)
    destination = models.CharField(max_length=255)
    heure_depart = models.TimeField(editable=True, null=True)
    places_disponibles = models.IntegerField()
    date = models.DateField(editable=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, null=True, editable=False)
    status = models.CharField(max_length=20, default=('completed', 'Terminé'),choices=[('ongoing', 'En cours'), ('completed', 'Terminé')])
   
    def __str__(self):
        return f"{self.point_depart} - {self.destination}"

class Categorie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_driver = models.BooleanField(default=False)

class Reservation(models.Model):
    STATUT_CHOICES = (
        ('Terminé', 'Terminé'),
        ('Confiirme', 'Confirme'),
        ('Annule', 'Annule'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    point_de_rencontre = models.CharField(max_length=255, null=True)
    places = models.PositiveIntegerField(null=True)
    statut= models.CharField(max_length=10, choices=STATUT_CHOICES, default='Confirme')
  

    def annuler_resvation(self):
        if self.statut == 'Confirme':
            self.statut = 'Annule'
            self.save()
    
    def terminer_reservation(self):
        if self.statut == 'Confirme':
            self.date > now
            self.statut = 'Terminé'
            self.save()
   
    def __str__(self):
        return f"{self.user} - {self.trajet}"


class Commentaire(models.Model):
    contenu = models.TextField()
    note = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.contenu

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






