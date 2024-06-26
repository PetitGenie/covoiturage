from django import forms
from covoiturage.models import Trajet, User

class LoginForm(forms.Form):
    username= forms.CharField()
    password= forms.CharField()


class ReserverForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    trajet = forms.ModelChoiceField(queryset=Trajet.objects.all())
    avance_paye = forms.DecimalField()
    

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

    class Meta:
        model = Trajet
        fields = '__all__'

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form_style'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form_style'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form_style'}))
    
class CommentaireForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    trajet = forms.ModelChoiceField(queryset=Trajet.objects.all())
    contenu= forms.CharField()
    note = forms.IntegerField()












