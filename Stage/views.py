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
                return redirect("/")
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
    now = datetime.now()
    reservations = Reservation.objects.filter(user=request.user)
    trajets = Trajet.objects.filter(date__gte=now.date(), places_disponibles__gt=0)

    # Mettre à jour le statut des réservations
    for reservation in reservations:
        if reservation.trajet.date < now.date():
            reservation.statut = 'terminé'
            reservation.save()
    Reservation.objects.filter(user=request.user, trajet__date__lt=now.date(), statut='confirmé').update(statut='terminé')

    selected_trajet = None

    if request.method == 'POST':
        # Récupérer les données du formulaire
        trajet_id = request.POST.get('trajet')
        places = int(request.POST.get('places', 0))
        point_de_rencontre = request.POST.get('point_de_rencontre')
        image = request.FILES.get('image')  

        # Vérifier si le nombre de places est positif
        if places <= 0:
            messages.error(request, "Le nombre de places doit être positif.")
            return redirect('reservation')

        # Récupérer le trajet sélectionné
        trajet = get_object_or_404(Trajet, id=trajet_id)

        # Vérifier si le nombre de places disponibles est suffisant
        if places > trajet.places_disponibles:
            messages.error(request, f"Désolé, il ne reste que {trajet.places_disponibles} places disponibles pour ce trajet.")
            return redirect('reservation')

        # Déterminer le statut en fonction de l'image
        if image:
            statut='Confirmée'
        else:
            statut='En attente'
            messages.success(request, f"Votre réservation de {places} place(s) a été effectuée mais reste en attente")

        # Créer une nouvelle réservation
        reservation = Reservation(
            user=request.user,
            trajet=trajet,
            places=places,
            point_de_rencontre=point_de_rencontre,
            timestamp=now,
            image=image,
            statut= statut
        )
        reservation.save()
        messages.success(request, f"Votre réservation de {places} place(s) a été effectuée avec succès.")

        # Mettre à jour le nombre de places disponibles pour le trajet
        trajet.places_disponibles -= places
        trajet.save()

        return redirect('reservation')

    else:  # GET request
        # Récupérer le trajet sélectionné (s'il y en a un)
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
            form.save() 
            messages.success(request, "Votre réservation a été modifiée avec succès.")
            return redirect('dashboard_driver')  
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
            
            # Vérifier que les places disponibles ne dépassent pas la capacité du véhicule
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

    all_trajets = Trajet.objects.all()
    for trajet in all_trajets:
        trajet.update_status()  

    trajets = Trajet.objects.filter(date__gte=now.date(), places_disponibles__gt=0)

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

def annulerT(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)

    # Annuler toutes les réservations confirmées pour ce trajet
    updated_count = Reservation.objects.filter(trajet=trajet, statut='Confirme').update(statut='Annulé')

    # Mettre à jour le statut du trajet
    trajet.statut = 'Annulé'
    trajet.save()

    # Message de confirmation
    messages.success(request, f"{updated_count} réservation(s) annulée(s).")

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

   

def dashboard_driver(request):
    trajets = Trajet.objects.filter(user=request.user)
    
    context = {'trajets': trajets}

    return render(request, 'dashboard_driver.html', context)


def verify(request):
    user = request.user

    # Vérifier si l'utilisateur a au moins une voiture enregistrée
    if Vehicule.objects.filter(user=user).exists():
        # Si l'utilisateur a une voiture, le rediriger vers la page des trajets
        return redirect('dashboard_driver')
    else:
        # Si l'utilisateur n'a pas de voiture, le rediriger vers la page d'ajout de voiture
        return redirect('addCar')

def addCar(request):
    if request.method == 'POST':
        form = CarForm(request, data=request.POST)
        if form.is_valid():
            # Récupérer les données du formulaire
            plaque = form.cleaned_data['plaque']
            modele = form.cleaned_data['modele']
            places = form.cleaned_data['places']
            color = form.cleaned_data['color']
            
            # Vérifier si le véhicule est déjà enregistré
            try:
                vehicle = Vehicule.objects.get(plaque=plaque)
                messages.warning(request, f'Le véhicule {modele} avec la plaque {plaque} est déjà enregistré.')
            except Vehicule.DoesNotExist:
                # Créer un nouveau véhicule et le sauvegarder
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

def facture(request, trajet_id):
    trajet = Trajet.objects.get(id=trajet_id)
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.trajet = trajet
            paiement.user = request.user
            paiement.save()
            return redirect('index')
    else:
        form = PaiementForm()
    return render(request, 'facture.html', {'form': form, 'trajet': trajet})