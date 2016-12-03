from django.shortcuts import redirect, render
from django.db import models
#from .models import  EchelonUser
from random import randint
from Crypto.PublicKey import RSA
from Crypto import Random
import requests

def home(request):
    return render(request, 'tracker/index.html', {})

def signedin(request):
    id_token = request.POST.get('TokenID')
    GoogleID = "867858739826-0j8s1vplsccuqcha9tng77pmrpc49mam.apps.googleusercontent.com"
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="+id_token
    response = requests.get(url)
    if response.json()['aud'] == GoogleID:
        try:
            #UserID = response.json()['sub']
            return render(request, 'tracker/Faliure.html', {'JSON': "All Good Here!"})
            #LoggedInUser = EchelonUser.objects.get(user_email=email)
            #userUrl = 'https://echelonportal.herokuapp.com/tracker/user/' + models.b64encode(LoggedInUser.user_index)
            #return redirect(userUrl)
        except:
            return render(request, 'tracker/Faliure.html', {'JSON': response.json()})
            #return NewUser(request,email)
            UserID = 0

    else:
        return render(request, 'tracker/Faliure.html', {})