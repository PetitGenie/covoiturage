from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, ReserverForm, TrajetForm, RegisterForm, CommentaireForm, CarForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from covoiturage.models import Trajet, Reservation, Commentaire, Categorie, Vehicule
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
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(user=request.user)
        now = datetime.now()
        trajets = Trajet.objects.filter(date__gte=now.date(), places_disponibles__gt=0)

        # Mettre à jour le statut des réservations
        for reservation in reservations:
            if reservation.trajet.date < now.date():
                reservation.statut = 'terminé'
                reservation.save()


        selected_trajet = None

        if request.method == 'POST':
            # Récupérer les données du formulaire
            trajet_id = request.POST.get('trajet')
            places = int(request.POST.get('places'))
            timestamp = request.POST.get('timestamp')
            point_de_rencontre = request.POST.get('point_de_rencontre')

            # Récupérer le trajet sélectionné
            trajet = Trajet.objects.get(id=trajet_id)
            selected_trajet = trajet

            # Vérifier si l'utilisateur a déjà une réservation pour ce trajet
            existing_reservation = Reservation.objects.filter(user=request.user, trajet=trajet).first()

            # Si l'utilisateur a déjà une réservation, augmenter le nombre de places
            if existing_reservation:
                existing_reservation.places +=places
                existing_reservation.save()

            # Sinon, créer une nouvelle réservation
            else:
                # Vérifier si le nombre de places disponibles est suffisant
                if places > trajet.places_disponibles:
                    messages.error(request, f"Désolé, il ne reste que {trajet.places_disponibles} places disponibles pour ce trajet.")
                    return redirect('reservation')

                # Créer une nouvelle réservation
                reservation = Reservation(
                    user=request.user,
                    trajet=trajet,
                    places=places,
                    point_de_rencontre=point_de_rencontre,
                    timestamp=timestamp,
                    statut='confirmé'
                )

                reservation.save()

                # Mettre à jour le nombre de places disponibles pour le trajet
                trajet.places_disponibles -= places
                trajet.save()

        # Récupérer le trajet sélectionné (s'il y en a un)
        if 'trajet' in request.GET:
            try:
                selected_trajet = Trajet.objects.get(id=request.GET.get('trajet'))
            except Trajet.DoesNotExist:
                pass

    else:
        reservations = []
        trajets = []
        selected_trajet = None

        return redirect('reservation')


    context = {
        'reservations': reservations,
        'trajets': trajets,
        'selected_trajet': selected_trajet,
    }
    return render(request, 'reserver.html', context)
'''
def annuler_resvation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    
    trajet = reservation.trajet
    
    trajet.places_disponibles += places
    trajet.save()
    
    reservation.delete()
    
    return redirect('reservation')
    '''
def create_trajet(request):
    if request.method == 'POST':
        form = TrajetForm(request.POST)
        if form.is_valid():
            trajet=form.save(commit=False)
            trajet.user= request.user
            trajet.save()
            return redirect("/dd/trajets")
            
            
    else:
        form = TrajetForm()
    
    context = {'form': form}
    return render(request, 'ajouterTrajet.html', context)

@login_required(login_url='/login/')
def trajets(request):
    now = datetime.now()
    trajets = Trajet.objects.filter(date__gte=now, places_disponibles__gt=0)
    
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
            return redirect('modifierT', trajet_id=trajet.id)
    else:
        form = TrajetForm(instance=trajet)

    return render(request, 'modifierT.html', {'form': form, 'trajet': trajet})

def deleteT(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)
    Reservation.objects.filter(trajet=trajet).update(statut='annulé')
    return redirect('dashboard_driver')



def commentaires(request):
    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            note = form.cleaned_data['note']
            if note < 1 or note > 10:
                form.add_error('note', 'La note doit être comprise entre 1 et 10.')
            else:
                comment = form.save(commit=False)
                comment.user = request.user
                comment.save()
                return redirect('/comment')
    else:
        form = CommentaireForm()

        comments = Commentaire.objects.all()
    context = {
        'form': form,
        'comments': comments
    }

    return render(request, 'commentaire.html', context)

   

def dashboard_driver(request):
    trajets = Trajet.objects.filter(user=request.user)
    
    context = {'trajets': trajets}

    return render(request, 'dashboard_driver.html', context)

def verify(request):
    try:
        vehicle = request.user.vehicle
        return redirect('dashboard_driver')
    except Vehicule.DoesNotExist:
        return redirect('addCar')


def addCar(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            # Vérifier si le véhicule est déjà enregistré
            plaque = form.cleaned_data['plaque']
            if not Vehicule.objects.filter(plaque=plaque).exists():
                form.save()
                messages.success(request, 'Véhicule ajouté avec succès!')
            else:
                messages.warning(request, 'Ce véhicule est déjà enregistré.')
            return redirect('dashboard_driver')
    else:
        form = CarForm()
    return render(request, 'vehicule.html', {'form': form})

def cars(request):
    vehicles = Vehicule.objects.all()
    return render(request, 'cars.html', {'vehicles': vehicles})

