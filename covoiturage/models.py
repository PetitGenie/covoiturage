from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vehicule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicules', null=True)
    modele = models.CharField(max_length=35, null=True)
    plaque = models.CharField(max_length=10, null=True)
    places = models.IntegerField(null=True)
    color = models.CharField(max_length=40, null=True)

    def __str__(self) -> str:
        return f"{self.modele} - {self.plaque} - {self.color}"

class Trajet(models.Model):
    point_depart = models.CharField(max_length=255)
    passe_par = models.CharField(max_length=255, null=True)
    destination = models.CharField(max_length=255)
    heure_depart = models.TimeField(editable=True, null=True)
    places_disponibles = models.IntegerField()
    date = models.DateField(editable=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, default='ongoing', choices=[('ongoing', 'En cours'), ('completed', 'Terminé')])

    def __str__(self) -> str:
        return f"{self.point_depart} - {self.destination}"
    
    def update_status(self):
        now = timezone.now()
        if self.date < now.date():
            self.status = 'completed'
        elif self.date == now.date() and self.heure_depart < now.time():
            self.status = 'completed'
        else:
            self.status = 'ongoing'
        self.save()
    
class Categorie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_driver = models.BooleanField(default=False)

class Reservation(models.Model):
    STATUT_CHOICES = (
        ('Terminer', 'Terminer'),
        ('Confirme', 'Confirme'),
        ('Annule', 'Annule'),
    )    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    point_de_rencontre = models.CharField(max_length=255, null=True)
    places = models.PositiveBigIntegerField(null=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='Confirme')
    image = models.ImageField(upload_to='reservations/', null=True, blank=True)

    def annuler_reservation(self):
        if self.statut == 'confirme':
            self.statut = 'annule'
            self.save()

    def terminer_reservation(self):
        if self.statut == 'confirme':
            self.date > now
            self.statut = 'termine'
            self.save()

    def update_status(self):
        now = timezone.now()
        if self.trajet.date < now.date():
            self.statut = 'Terminer'
        elif self.statut == 'Annule':
            pass  # Le statut reste annulé
        else:
            self.statut = 'Confirme'
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
    montant = models.PositiveBigIntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user} - {self.montant}"
