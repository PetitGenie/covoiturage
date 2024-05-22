
from django.contrib import admin
from .models import  Trajet, Reservation, Commentaire,  Notification, Paiement

class TrajetAdmin(admin.ModelAdmin):
    list_display = ('point_depart', 'destination', 'heure_depart', 'places_disponibles', 'plaque','modele' ,'user')
    list_filter = ('heure_depart', 'user')
    search_fields = ('point_depart', 'destination')

    def conducteur(self, obj):
        return obj.ref_conducteur_trajet.nom

    conducteur.short_description = 'Conducteur'


admin.site.register(Trajet, TrajetAdmin)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'trajet','date', 'avance_payee')
    def user(self, obj):
      if user.is_connected:
        return obj.user.username
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Commentaire)


admin.site.register(Notification)
admin.site.register(Paiement)
