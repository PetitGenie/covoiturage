from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, ReserverForm, TrajetForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from covoiturage.models import Trajet, Reservation
from datetime import datetime

def index(request):
   
    return render(request, "index.html", locals()) 

from django.shortcuts import render, redirect
from .forms import RegisterForm

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
    else:
        reservations = []

    context = {'reservations': reservations}
    return render(request, 'reserver.html', context)


def createReservation(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)

    if request.method == 'POST':
        nom = request.POST['nom']
        email = request.POST['email']

        reservation = Reservation.objects.create(
            trajet=trajet,
            nom=nom,
            email=email
        )
        return redirect('/reservation', reservation_id=reservation.id)

    return render(request, 'reserver.html', {'trajet': trajet})

def create_trajet(request):
    if request.method == 'POST':
        form = TrajetForm(request.POST)
        if form.is_valid():
            trajet=form.save(commit=False)
            trajet.user= request.user
            trajet.save()
            return redirect("/trajets")
            
    else:
        form = TrajetForm()
    
    context = {'form': form}
    return render(request, 'ajouterTrajet.html', context)

@login_required(login_url='/login/')
def trajets(request):
    now = datetime.now()
    trajets = Trajet.objects.filter(date__gte=now)

    context = {'trajets': trajets}
    return render(request, 'trajet.html', context)

def comments(request):
    return render(request, 'commentaire.html')
