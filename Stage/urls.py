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
from .views import index
from . import views
from .views import reservation, createtrajet
from .views import Trajet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('covoiturage/', include('covoiturage.urls')),
    path('', index),
     path('login/', views.connexion, name='login'),
    path('logout/', views.deconnexion, name='logout'),
    path('reservation/', reservation, name='reservation'),
    path('trajet/', views.trajetdetails, name='trajet'),
    path('trajet/', views.createtrajet, name='createtrajet'),
    path('commentaires/', views.commentaire, name='commentaire'),
    path('reservation/', views.create_reservation, name='create_reservation'),
    path('register/', views.register, name='register'),
]
