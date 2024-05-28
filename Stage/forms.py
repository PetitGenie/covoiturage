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
    heure_depart = forms.DateTimeField(widget = forms.DateInput(format= "%Y-%m-%d %H:%M"))
    class Meta:
        model = Trajet
        fields = '__all__' 


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form_style'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form_style'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form_style'}))











