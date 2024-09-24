from django import forms
from covoiturage.models import Trajet, User, Commentaire, Vehicule, Paiement, Reservation
from django.utils import timezone

class LoginForm(forms.Form):
    username= forms.CharField()
    password= forms.CharField()


class ReserverForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=False)
    trajet = forms.ModelChoiceField(queryset=Trajet.objects.all())
    places = forms.DecimalField()
    point_de_rencontre = forms.CharField()
    image = forms.ImageField()
    class Meta:
        model = Reservation 
        fields = ['trajet', 'places', 'point_de_rencontre', 'image'] 
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user 
            self.instance.user = user  
            self.fields['user'].widget.attrs['readonly'] = 'readonly'

class TrajetForm(forms.ModelForm):
    class Meta:
        model = Trajet
        fields = [
            'point_depart',
            'passe_par',
            'destination',
            'places_disponibles',
            'vehicule',
            'heure_depart',
            'date',
        ]
        widgets = {
            'point_depart': forms.TextInput(attrs={'required': 'true'}),
            'passe_par': forms.TextInput(attrs={'required': 'false'}),
            'destination': forms.TextInput(attrs={'required': 'true'}),
            'vehicule': forms.Select(attrs={'required': 'true'}),
            'places_disponibles': forms.NumberInput(attrs={'min': 1, 'required': 'true'}),
            'heure_depart': forms.TimeInput(attrs={'type': 'time', 'required': 'true'}),
            'date': forms.DateInput(attrs={'type': 'date', 'required': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TrajetForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['vehicule'].queryset = user.vehicules.all()

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form_style'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form_style'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form_style'}))
    

class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu', 'note', 'trajet']
        widgets = {
            'contenu': forms.Textarea(attrs={'required': 'true', 'placeholder': 'Votre commentaire...'}),
            'note': forms.NumberInput(attrs={'min': 1, 'max': 10, 'required': 'true'}),
            'trajet': forms.Select(attrs={'required': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CommentaireForm, self).__init__(*args, **kwargs)

        if user:
            # Filter completed reservations by the user
            reservations = Reservation.objects.filter(user=user, statut='terminé') 
            trajets = reservations.values_list('trajet_id', flat=True)
            # Filter trajets based on the user's completed reservations
            self.fields['trajet'].queryset = Trajet.objects.filter(id__in=trajets)

            if not self.fields['trajet'].queryset.exists():
                self.fields['trajet'].empty_label = "Aucun trajet disponible"


class CarForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    modele = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form_style'}))
    places = forms.IntegerField()
    plaque = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form_style'}))
    color = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form_style'}))

    class Meta:
        model = Vehicule
        fields = ['user', 'modele', 'plaque', 'color']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].initial = request.user
        self.fields['user'].queryset = User.objects.filter(pk=request.user.pk)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.cleaned_data['user']
        if commit:
            instance.save()
        return instance






class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['montant', 'date']