from django.shortcuts import render, redirect
from .forms import LoginForm, ReserverForm, TrajetForm,UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from covoiturage.models import Trajet

def index(request):
   
    return render(request, "index.html", locals()) 

def register(request):
    register_form = UserForm()
    return render(request, 'inscription.html', locals())

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
    if request.method == "POST":
        connection_form = ReserverForm(request.POST)
        if connection_form.is_valid():
            user = connection_form.cleaned_data['user']
            trajet = connection_form.cleaned_data['trajet']
            avance_paye = connection_form.cleaned_data['avance_paye']

            return redirect("/")
        else:
            error_message = "Sorry, we didn't recognize you."

            connection_form.add_error(None, error_message)
    else:
        connection_form = ReserverForm()
    
    context = {'connection_form': connection_form}
    return render(request, 'reserver.html', context)

@login_required(login_url='/login/')
def create_trajet(request):
    if request.method == 'POST':
        form = TrajetForm(request.POST)
        if form.is_valid():
            trajet=form.save(commit=False)
            trajet.user= request.user
            trajet.save()
            return redirect("/")
            
    else:
        form = TrajetForm()
    
    context = {'form': form}
    return render(request, 'trajet.html', context)
def trajets(request):
    trajets = Trajet.objects.all()  
    context = {'trajets': trajets}
    return render(request, 'trajet.html', context)