from django.contrib import admin
from .models import Vehicule, Trajet, Reservation, Commentaire, Notification, Paiement, Categorie
admin.site.site_header = ('JANA NANJE')
admin.site.site_title = ('JANA_NANJE Administration')
class TrajetAdmin(admin.ModelAdmin):
    list_display = ('user','point_depart', 'passe_par', 'destination', 'heure_depart', 'places_disponibles', 'date','telephone' , 'vehicule', 'status')
    list_filter = ('heure_depart', 'user', 'destination')
    search_fields = ('point_depart', 'destination')

    def get_vehicule(self, obj):
        return obj.Vehicule if obj.Vehicule else 'Pas de véhicule'
    get_vehicule.short_description = 'Véhicule'

    def save_model(self, request, obj, form, change):
        if not change:
            # Check if there are enough available places in the trajet
            places_requested = form.cleaned_data.get('places', 0)
            if places_requested > obj.places_disponibles:
                # Raise an error if there are not enough available places
                raise ValueError(f"There are only {obj.places_disponibles} available places in this trajet.")
            
            # Update the places_disponibles
            obj.places_disponibles -= places_requested
        
        # Set the trajet as done if all places are reserved
        if obj.places_disponibles == 0:
            obj.status = 'completed'
        
        # Call the parent's save_model method
        super().save_model(request, obj, form, change)

admin.site.register(Trajet, TrajetAdmin)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'trajet','places','timestamp', 'point_de_rencontre','avance','statut')
    search_fields = ('timestamp','places','point_de_rencontre')

admin.site.register(Reservation, ReservationAdmin)
class VehiculeAdmin(admin.ModelAdmin):
    list_display=('modele','places','plaque','color')
admin.site.register(Vehicule, VehiculeAdmin)
class CommentaireAdmin(admin.ModelAdmin):
      list_display=('user', 'trajet','contenu','note')
admin.site.register(Commentaire, CommentaireAdmin)      
admin.site.register(Notification)
class PaiementAdmin (admin.ModelAdmin):
    list_display = ('paiement','code_confirmation', 'timestamp')
admin.site.register(Paiement, PaiementAdmin)    