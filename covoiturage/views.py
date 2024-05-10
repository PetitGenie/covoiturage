from django.shortcuts import render, get_object_or_404
from .models import Trajet




def index(request):
    return render(request, "index.html", locals())    

