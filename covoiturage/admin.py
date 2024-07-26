from django.contrib import admin
from .models import Vehicule, Trajet, Reservation, Commentaire, Notification, Paiement

class TrajetAdmin(admin.ModelAdmin):
    list_display = ('point_depart', 'destination', 'heure_depart', 'date','places_disponibles','user','status')
    list_filter = ('heure_depart', 'user')
    search_fields = ('point_depart', 'destination')

    def conducteur(self, obj):
        return obj.ref_conducteur_trajet.nom

def save_model(self, request, trajet: Trajet, form, change):
    if not change:
        # Check if there are enough available places in the trajet
        places_requested = form.cleaned_data['places']
        if places_requested > trajet.places_disponibles:
            # Raise an error if there are not enough available places
            raise ValueError(f"There are only {trajet.places_disponibles} available places in this trajet.")
        
        # Update the places_disponibles
        trajet.places_disponibles -= places_requested
        trajet.save()

    # Set the trajet as done if all places are reserved
    if trajet.places_disponibles == 0:
        trajet.done = True
        trajet.save()

    # Call the parent's save_model method
    super().save_model(request, trajet, form, change)

admin.site.register(Trajet, TrajetAdmin)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'trajet','places','date', 'avance_payee')

admin.site.register(Reservation, ReservationAdmin)
class VehiculeAdmin(admin.ModelAdmin):
    list_display=('modele', 'plaque','color')
admin.site.register(Vehicule)
class CommentaireAdmin(admin.ModelAdmin):
      list_display=('user', 'trajet','contenu','note')
admin.site.register(Commentaire, CommentaireAdmin)      
admin.site.register(Notification)
admin.site.register(Paiement)