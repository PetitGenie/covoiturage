from django import forms
from covoiturage.models import Trajet, User, Commentaire, Vehicule, Paiement


class LoginForm(forms.Form):
    username= forms.CharField()
    password= forms.CharField()


class ReserverForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    trajet = forms.ModelChoiceField(queryset=Trajet.objects.all())
    places = forms.DecimalField()
    point_de_rencontre = forms.DecimalField()

class TrajetForm(forms.ModelForm):
    heure_depart = forms.TimeField(
        widget=forms.TimeInput(
            attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': 'Heure de départ',
                'icon': 'fas fa-clock'
            }
        )
    )
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Date',
                'icon': 'fas fa-calendar-alt'
            }
        )
    )
    vehicule = forms.ModelChoiceField(queryset=Vehicule.objects.all(), initial=Vehicule.objects.last())
    passe_par= forms.CharField()
    class Meta:
        model = Trajet
        fields = '__all__'

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form_style'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form_style'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form_style'}))
    
class CommentaireForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    trajet = forms.ModelChoiceField(queryset=Trajet.objects.all())
    contenu= forms.CharField()
    note = forms.IntegerField()
    class Meta:
        model = Commentaire
        fields = '__all__'

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



class CarForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    modele = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form_style'}))
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