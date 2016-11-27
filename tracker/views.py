from django.shortcuts import redirect, render
from django.db import models
#from .models import  EchelonUser
from random import randint
import requests

def home(request):
    return render(request, 'tracker/index.html', {})

def signedin(request):
    id_token = request.POST.get('TokenID')
    email = request.POST.get('Email')
    GoogleID = request.POST.get('googleid')
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="+id_token
    response = requests.get(url)
    if response.json()['aud'] == GoogleID:
        try:
            #LoggedInUser = EchelonUser.objects.get(user_email=email)
            #userUrl = 'https://echelonportal.herokuapp.com/tracker/user/' + models.b64encode(LoggedInUser.user_index)
            #return redirect(userUrl)
        except:
            return NewUser(request,email)

    else:
        return render(request, 'tracker/faliure.html', {})