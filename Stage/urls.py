"""
URL configuration for Stage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import index
from . import views
from .views import reservation
from .views import Trajet,deleteT, annulerT,modifierT, dashboard_driver, addCar, commentaires, paiement

urlpatterns = [
    path('admin/', admin.site.urls),
    path('covoiturage/', include('covoiturage.urls')),
    path('', index),
    path('login/', views.logins, name='login'),
    path('logout/', views.deconnexion, name='logout'),
    path('reservation/', views.reservation, name='reservation'),
    path('trajet/', views.trajets, name='trajet'),
    path('login/trajet/', views.trajets, name='trajet'),
    path('dd/trajets/', views.create_trajet, name='trajet'),
    path('register/', views.register, name='register'),
    path('dashboard_driver/<int:trajet_id>/annuler/', views.annulerT, name='annulerT'),
    path('dashboard_driver/<int:trajet_id>/supprimer/', views.deleteT, name='deleteT'),
    path('annuler-reservation/<int:reservation_id>/', views.annuler_reservation, name='annuler_reservation'),
    path('reservation/<int:trajet_id>/createReservation/reservation', views.reservation, name='reservation'),
    path('trajet/<int:trajet_id>/modifier/', views.modifierT, name='modifierT'),
    path('reservation/<int:reservation_id>/modifier/', views.modifierR, name='modifierR'),
    path('comments/', views.commentaires, name='commentaires'),
    path('verify/', views.verify, name='verify'),
    path('vehicle/add/', views.addCar, name='addCar'),
    path('cars/vehicle/add/', views.addCar, name='addCar'),
    path('cars/', views.cars, name='cars'),
    path('dashboard_driver/', views.dashboard_driver, name='dashboard_driver'),
    path('paiement/<int:reservation_id>', views.paiement, name='paiement'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)