from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, ReserverForm, TrajetForm, RegisterForm, CommentaireForm, CarForm, PaiementForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from covoiturage.models import Trajet, Reservation, Commentaire, Categorie, Vehicule, Paiement
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from datetime import datetime, timedelta
import random
import string

def index(request):
   
    return render(request, "index.html", locals()) 

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            name = register_form.cleaned_data['name']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            
            try:
                user = User.objects.create_user(username=name, email=email, password=password)
                user.save()
                return redirect('login')
            except Exception as e:
                register_form.add_error(None, str(e))
    else:
        register_form = RegisterForm()

    return render(request, 'register.html', {'register_form': register_form})

from django.contrib.auth import authenticate, login
from .forms import LoginForm

def logins(request):
    connection_form = LoginForm()
    erreur = ""

    if request.method == "POST":
        connection_form = LoginForm(request.POST)
        if connection_form.is_valid():
            username = connection_form.cleaned_data['username']
            password = connection_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('trajet/')
            else:
                erreur = "We didn't recognize you"
        else:
            erreur = "Invalid login credentials"
    
    return render(request, "login.html", {'connection_form': connection_form, 'erreur': erreur})       

def deconnexion(request):
    logout(request)
    return redirect("/") 
         
@login_required(login_url='/login/')
def reservation(request):
    now = timezone.now()
    reservations = Reservation.objects.filter(user=request.user)
    trajets = Trajet.objects.filter(date__gte=now.date(), places_disponibles__gt=0).exclude(user=request.user)
    trajets = trajets.exclude(date=now.date(),heure_depart__lt=now.time())
    selected_trajet = None
    # Mettre à jour le statut des réservations
    for reservation in reservations:
        if (reservation.trajet.date < now.date()) or (reservation.trajet.date == now.date() and reservation.trajet.heure_depart < now.time()):
            reservation.statut = 'terminé'
            reservation.save()

    if request.method == 'POST':
        places = int(request.POST.get('places', 0))
        point_de_rencontre = request.POST.get('point_de_rencontre')
        trajet = Trajet.objects.get(id=request.POST.get('trajet'))

        if places > trajet.places_disponibles:
            messages.error(request, "Le nombre de places demandées dépasse les places disponibles.")
            return redirect('reserver')

        confirmation_code = generate_confirmation_code() 
        reservation = Reservation(
            user=request.user,
            trajet=trajet,
            places=places,
            point_de_rencontre=point_de_rencontre,
            timestamp=now,
            statut='en attente',
            confirmation_code=confirmation_code,
        )
        reservation.save()

        # Mettre à jour les places disponibles
        trajet.places_disponibles -= places
        trajet.save()

        messages.success(request, f"Votre réservation de {places} place(s) a été effectuée avec succès. Copiez ce code de confirmation : {confirmation_code}")
        
        return redirect('reservation')

    else: 
        trajet_id = request.GET.get('trajet')
        if trajet_id:
            try:
                selected_trajet = Trajet.objects.get(id=trajet_id)
            except Trajet.DoesNotExist:
                selected_trajet = None

    context = {
        'reservations': reservations,
        'trajets': trajets,
        'selected_trajet': selected_trajet,
    }
    return render(request, 'reserver.html', context)
        
def modifierR(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if request.method == 'POST':
        form = ReserverForm(request.POST, request.FILES, instance=reservation, user=request.user)
        if form.is_valid():
            # Récupérer le nombre de places réservées avant la modification
            places_reservees_avant = reservation.places  
            # Enregistrer la nouvelle réservation
            reservation = form.save(commit=False)
            # Récupérer le nombre de places réservées après la modification
            places_reservees_apres = reservation.places  
            
            # Mettre à jour les places disponibles
            places_diff = places_reservees_apres - places_reservees_avant
            reservation.trajet.places_disponibles -= places_diff  
            reservation.trajet.save()  
            reservation.save() 
            messages.success(request, "Votre réservation a été modifiée avec succès.")
            return redirect('reservation')  
    else:
        form = ReserverForm(instance=reservation, user=request.user)

    return render(request, 'modifierR.html', {'form': form, 'reservation': reservation})


def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    trajet = reservation.trajet
    trajet.places_disponibles += reservation.places
    trajet.save()
    
    reservation.statut = 'annulé'
    reservation.save()
    
    messages.success(request, "Réservation annulée avec succès.")
    return redirect('reservation')

def create_trajet(request):
    if request.method == 'POST':
        form = TrajetForm(request.POST, user=request.user)
        if form.is_valid():
            trajet = form.save(commit=False)
            trajet.user = request.user
            
            # Vérification de la date pour définir le statut
            if trajet.date < timezone.now().date():
                trajet.status = 'terminé'
            else:
                trajet.status = 'en cours'  
            
          
            vehicule = trajet.vehicule  
            if trajet.places_disponibles > vehicule.places:  
                messages.error(request, "Le nombre de places disponibles ne peut pas dépasser la capacité du véhicule.")
                return render(request, 'ajouterTrajet.html', {'form': form})

            trajet.save()
            messages.success(request, "Trajet créé avec succès.")

            return redirect('dashboard_driver')  
    else:
        form = TrajetForm(user=request.user)

    return render(request, 'ajouterTrajet.html', {'form': form})

@login_required(login_url='/login/')
def trajets(request):
    now = timezone.now()

    trajets = Trajet.objects.filter(date__gte=now.date(), places_disponibles__gt=0)
    trajets = trajets.exclude(user=request.user)
    trajets = trajets.exclude(date=now.date(),heure_depart__lt=now.time())
    context = {'trajets': trajets}
    return render(request, 'trajet.html', context)

def modifierT(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id, user=request.user)

    if request.method == 'POST':
        form = TrajetForm(request.POST, instance=trajet)
        if form.is_valid():
            trajet = form.save(commit=False)
            trajet.user = request.user
            trajet.save()
            return render(request,'dashboard_driver.html')
    else:
        form = TrajetForm(instance=trajet)

    return render(request, 'modifierT.html', {'form': form, 'trajet': trajet})

def deleteT(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)
    Reservation.objects.filter(trajet=trajet).update(statut='annulé')
    return redirect('dashboard_driver')




def commentaires(request):
    if request.method == 'POST':
        form = CommentaireForm(request.POST, user=request.user) 
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.user = request.user  
            commentaire.save()
            return redirect('comments') 
    else:
        form = CommentaireForm(user=request.user)  

    return render(request, 'commentaire.html', {'form': form})

def annulerT(request):
        if request.method == 'POST' and 'annuler' in request.POST:
           trajet_id = request.POST.get('trajet_id')
        try:
            trajet = Trajet.objects.get(id=trajet_id, user=request.user)
            trajet.status = 'annulé'
            trajet.save()
            messages.success(request, f"{updated_count} réservation(s) annulée(s).")
        except Trajet.DoesNotExist:
            pass

        context = {'trajets': trajets}
        return render(request, 'dashboard_driver.html', context)

def dashboard_driver(request):
    trajets = Trajet.objects.filter(user=request.user)
    now = timezone.now()

    for trajet in trajets:
        heure_depart = timezone.make_aware(datetime.combine(now.date(), trajet.heure_depart))
        if heure_depart < now:
            trajet.status = 'terminé'
            trajet.save()

    context = {'trajets': trajets}
    return render(request, 'dashboard_driver.html', context)


def verify(request):
    user = request.user

    if Vehicule.objects.filter(user=user).exists():
        return redirect('cars')
    else:
       
        return redirect('addCar')

def addCar(request):
    if request.method == 'POST':
        form = CarForm(request, data=request.POST)
        if form.is_valid():
            plaque = form.cleaned_data['plaque']
            modele = form.cleaned_data['modele']
            places = form.cleaned_data['places']
            color = form.cleaned_data['color']

            try:
                vehicle = Vehicule.objects.get(plaque=plaque)
                messages.warning(request, f'Le véhicule {modele} avec la plaque {plaque} est déjà enregistré.')
            except Vehicule.DoesNotExist:
        
                vehicle = Vehicule(
                    user=request.user,
                    plaque=plaque,
                    modele=modele,
                    places=places,
                    color=color
                )
                vehicle.save()
                messages.success(request, 'Véhicule ajouté avec succès!')
            
            return redirect('dashboard_driver')
    else:
        form = CarForm(request)
    
    return render(request, 'vehicule.html', {'form': form})
    
def cars(request):
    vehicles = Vehicule.objects.filter(user=request.user)
    return render(request, 'cars.html', {'vehicles': vehicles})

def paiement(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)    
    if request.method == 'POST':
        form = PaiementForm(request.POST, request.FILES)
        if form.is_valid():
            paiement_instance=form.save()

            reservation.avance = paiement_instance.paiement
            reservation.statut= 'confirmé'
            reservation.save()    
            return redirect('reservation')  
    else:
        form = PaiementForm()

    return render(request, 'paiement.html', {'form': form})

def generate_confirmation_code(length=8):
   
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def notif(request):
    if not request.user.is_authenticated:
        messages.error(request, "Vous devez être connecté pour voir vos réservations.")
        return redirect('login')  

    trajets = Trajet.objects.filter(user=request.user)
    reservations = Reservation.objects.filter(trajet__in=trajets)

    return render(request, 'notifications.html', {
        'reservations': reservations,
    })  

def my_payment(request):
    if request.user.is_authenticated:
        payments = Paiement.objects.filter(user=request.user)
    else:
        payments = []

    return render(request, 'my_payment.html', {'payments': payments})    