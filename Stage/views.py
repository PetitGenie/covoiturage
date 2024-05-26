from django.shortcuts import render, redirect
from .forms import LoginForm, ReserverForm, TrajetForm, CommentaireForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from covoiturage.models import Trajet, Reservation


def index(request):
   
    return render(request, "index.html", locals()) 




def connexion(request):
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


def reservationDetails(request):
    reservation = Reservation.objects.filter(user=request.user)
    context = {'reservation': reservation}
    return render(request, 'reserver.html', context)



def create_reservation(request, trajet_id):
    if request.method == 'POST':
        trajet = Trajet.objects.get(id=trajet_id)
        print(f"Trajet récupéré : {trajet}")
        reservation = Reservation(
            user=request.user,
            trajet=trajet,
           
        )
        try:
            reservation.full_clean()  
            print(f"Réservation créée : {reservation}")
            reservation.save()
            print(f"Réservation enregistrée")
            return redirect('reservation_list')
        except Exception as e:
          
            print(f"Erreur lors de la création de la réservation: {e}")
            return render(request, 'trajet.html', {'trajet': trajet, 'error_message': "Une erreur est survenue lors de la création de la réservation."})
    else:
        trajet = Trajet.objects.get(id=trajet_id)
        print(f"Trajet récupéré : {trajet}")
        return render(request, 'trajet.html', {'trajet': trajet})

def createtrajet(request):
    if request.method == 'POST':
        form = TrajetForm(request.POST)
        if form.is_valid():
            trajet=form.save(commit=False)
            trajet.user= request.user
            trajet.save()
            return redirect("/trajet")
            
    else:
        form = TrajetForm()
    
    context = {'form': form}
    return render(request, 'ajouterTrajet.html', context)

@login_required(login_url='/login')
def trajetdetails(request):
    trajets = Trajet.objects.all()
    context = {'trajet': trajets}
    return render(request, 'trajet.html', context)

def commentaire(request):
    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire=form.save(commit=False)
            commentaire.user= request.user
            commentaire.save()
            return redirect("/commentaires")
            
    else:
        form = CommentaireForm()
    
    context = {'form': form}
    return render(request, 'commentaire.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        
        if password != password_confirm:
            return render(request, 'register.html', {'error': 'Les mots de passe ne correspondent pas.'})
        
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('accueil')
        except:
            return render(request, 'register.html', {'error': 'Erreur lors de la création du compte.'})
    
    return render(request, 'register.html')    