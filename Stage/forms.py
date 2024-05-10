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
    heure_depart = forms.DateTimeField(widget = forms.DateInput(format= "%Y-%m-%d"))
    class Meta:
        model = Trajet
        fields = '__all__' 












