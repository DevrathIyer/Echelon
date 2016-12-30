from django.shortcuts import redirect, render
from django.db import models
from django.http import HttpResponse,Http404
from random import randint
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random
import base64
import requests
import os
f = """-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,2F5252FFFF575D73

EAOm5SztxVoaNQgh0PyR0FZlyJM5Hdyz+GL/GVQyJjaUFMmOkDTUsNcv8k4AzB7V
9yz0gpWajwQCqJDfC3u9FO8PtPKisqvB1/cy0QfAvODND6XapYotav94K8y2ape2
2amfaifN0Nci/DnbU5t5trwRyh6A/iC2RVTFuqssFMFDUMagXbzgD56stb0n6ccF
NqprkbNNN/ICaFG+YcwX0Pr5i2EaSiqP/6a9+seK0cf+/tU4Uc43Rbgzj8jxAWkM
nb0ufGPmV0U2a5i3G7/4Vh/1/HQa8uLYDvANCpknuWyV1qvU8ez+KF2iSo+WNApi
avEi785Rw8hzA1OOnxkYsPp1Klrj5xPMZBv45MF4PLji32K37BvFNhxM7svtotmi
akyVmLLwBnSjqWW48e9s0iFMcreVKSwG03uCq/s4iXJFdxLPp3NVU3I+nb3BPdeV
dQRsV6M/eDMsvhXuAx7d7wMkl6cB0rOxbZ2Gxmvwwx1tT70NtAJFtCPIkx3JDEOH
bBynvMdKBP43cGfjSYpcnUtVlgRTCRFxiQgd8ozIDe+I7zUAhDFiLdksiHidM75O
vB3AnkiLTmsesPixMABd6peL/d1dKDEe+yhr02mhwLFx/6aV4eRU2PTzJudHNHOD
hJ5Dc2o0vDI/1hSY02boI5qqgllWfkB8zhSkcrn+o6nt59zPEidiuxPVkFtd+K15
dzPNi+br/cLPatcQlDLlt/mNIK4LmJVzIGxgspvEN1hO2toh7gEBfQafMRo+o7Yo
z5bAgAD303S3Hp2J0zb3F7UAP0GjlBO3dm+wDJJibSTVFeLOAPMNBQitHcxpAK/L
lscegz/u/qyHvxwDNtlVzJcU1c7N6sgl22kM//t5NVumay1wztUeUoKblyu+Ejlw
wMWYu/f789QanN81tWRVHVCdpH84UnRVEif0BvTIhho+zF7XHNaMrQCPbZwoz2O9
GwbWcadgdKrGjfGO6nV2OPSMEL8q+4k2K2iaVQNWWPkFtmiT2v38mwBBuIt3UL7T
t7sbwATQCg3+PmnBmX6NmYKUllzQfaN+0X74vuPXdEpTtS4AG/u5KL6KB0H/VzzN
zMqVDV3IqoVZtDn3zE5ssh9I61g0U5FByq42AfAKKQd92Asw2bdmJoT+uMzOqbI1
N0gZXIDIi1XWGjygv/9mIWyuljqLRwNPtRE59eNsb2MuQeCH9UBSUPWHHBfyNmpY
WNQ8bjaHmASR0Kba9GugyHdVoNkNKDflSDpkr3VCiSOJewN58MujTOi4HVdgU05o
2vExDYHBzV/wAZXiuNO8nd/bRRJKjhZ/IH3vusz/kzw9fNQjrcLTwb8TCceTvOlG
ZpUSJbN/0oFtbGidplSODGdyRaZ9lHSNA4ylS4S9c1U8Hv/zC+ZHOa8OMAhS2CKG
YA3OpZujVRdQPeodBCqFocvEjEwWhPzpxN/Q3/bMX9gvEZNSjl2N5ms7EkxRqQmA
2GwN4EvxUrfa+xUMXd1mPz0h2V5vY0RUhiZx08DcTE2yHw5jf3kf758tgUb/e3EH
YZwZkOfXiUuP0/8ff94r4B23WE3kAxJXj09IiANe6aX9WJtcGNbhqCNU9hgRMu2h
-----END RSA PRIVATE KEY-----"""
r = RSA.importKey(f, passphrase=os.environ['ENCRYPTION_PASSWORD'])
os.environ['ENCRYPTION_PASSWORD']
string = 'hello'  # base64.b64encode(bytes('hello'))
hash = SHA256.new(string).digest()
data = r.sign(hash, 32)

def home(request):
    return render(request, 'tracker/Homepage.html', {})

def login(request):
    return render(request, 'tracker/Login.html', {})

def signup(request):
    return render(request, 'tracker/NewUser.html', {})

def credits(request):
    try:
        id_token = request.session['TokenID']
    except:
        return Http404()
    GoogleID = "867858739826-0j8s1vplsccuqcha9tng77pmrpc49mam.apps.googleusercontent.com"
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=" + id_token
    response = requests.get(url)
    if response.json()['iss'] in ('accounts.google.com', 'https://accounts.google.com'):
        if response.json()['aud'] == GoogleID:
            response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getUserData', data=post_data)
            if response.json()['error'] == "NA":
                UserCredits = response.json()['credits']
            return render(request, 'tracker/Credits.html', {})

def createnewuser(request):
    id_token = request.POST.get('TokenID')
    GoogleID = "867858739826-0j8s1vplsccuqcha9tng77pmrpc49mam.apps.googleusercontent.com"
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="+id_token
    response = requests.get(url)
    if response.json()['iss'] in ('accounts.google.com', 'https://accounts.google.com'):
        if response.json()['aud'] == GoogleID:
            #response['auth'] = os.environ['password']
            userid = response.json()['sub']
            name = response.json()['name']
            email = response.json()['email']
            post_data = {'auth': os.environ['password'], 'uid': userid, 'name': name , 'email': email}
            response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/createUser', data=post_data)
            return render(request, 'tracker/NewUser.html', {'JSON': response.json()})
        else:
            return render(request, 'tracker/Faliure.html', {})
    else:
        return render(request, 'tracker/Faliure.html', {})

def viewuserdata(request):
    id_token = request.POST.get('TokenID')
    request.session['TokenID'] = id_token
    GoogleID = "867858739826-0j8s1vplsccuqcha9tng77pmrpc49mam.apps.googleusercontent.com"
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token="+id_token
    response = requests.get(url)
    if response.json()['iss'] in ('accounts.google.com', 'https://accounts.google.com'):
        if response.json()['aud'] == GoogleID:
            #response['auth'] = os.environ['password']
            userid = response.json()['sub']
            post_data = {'auth': os.environ['password'], 'uid': userid}
            response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getUserData', data=post_data)
            if response.json()['error'] == "NA":
                UserName = response.json()['name']
                UserCredits = response.json()['credits']
                post_data = {'auth': os.environ['password'], 'uid': userid}
                response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getUserProjects', data=post_data)
                Projects = response.json()['project_list'].split()
                ProjectNumber = len(Projects)
                ProjectList = ['' for x in range(ProjectNumber)]
                for x in range(ProjectNumber):
                        post_data = {'auth': os.environ['password'], 'projectid': Projects[x]}
                        response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getProjectInfo',
                                                 data=post_data)
                        ProjectList[x] = response.json()
                return render(request, 'tracker/Projects.html', {'Projects': ProjectList,'Number':range(ProjectNumber),'UserName':UserName})
        else:
            return render(request, 'tracker/Faliure.html', {})
    else:
        return render(request, 'tracker/UserPortal.html', {})