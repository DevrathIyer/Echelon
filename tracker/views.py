from django.shortcuts import redirect, render
from django.db import models
from django.http import HttpResponse,Http404
import json
from random import randint
import bcrypt
import base64
import requests
import os
import random, string

def home(request):
    return render(request, 'tracker/Homepage.html', {})

def login(request):
    return render(request, 'tracker/Login.html', {})

def signup(request):
    return render(request, 'tracker/NewUser.html', {})

def signout(request):
    try:
        id_token = request.session['TokenID']
    except:
        return Http404()
    request.session.flush()
    return redirect('login')

def addcredits(request):
    try:
        id_token = request.session['TokenID']
    except:
        return HttpResponse(json.dumps({'status': 'NAH'}), content_type='application/json')
    GoogleID = "867858739826-0j8s1vplsccuqcha9tng77pmrpc49mam.apps.googleusercontent.com"
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=" + id_token
    response = requests.get(url)
    if response.json()['iss'] in ('accounts.google.com', 'https://accounts.google.com'):
        if response.json()['aud'] == GoogleID:
            userid = response.json()['sub']
            post_data = {'auth': os.environ['password'], 'uid': userid, 'numcredits': 1000}
            response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/addCredits', data=post_data)
            return HttpResponse(json.dumps({'message': response.json()['message']}), content_type='application/json')

def checkproject(request):
    try:
        id_token = request.session['TokenID']
        projectid = request.POST.get('projectid')
    except:
        return HttpResponse(json.dumps({'status': 'NAH'}), content_type='application/json')
    GoogleID = "867858739826-0j8s1vplsccuqcha9tng77pmrpc49mam.apps.googleusercontent.com"
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=" + id_token
    response = requests.get(url)
    if response.json()['iss'] in ('accounts.google.com', 'https://accounts.google.com'):
        if response.json()['aud'] == GoogleID:
            post_data = {'auth': os.environ['password'], 'projectid': projectid}
            response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getProjectInfo', data=post_data)
            if (response.json()['message'] == 'could not get project info'):
                return render(request, 'ProjectCheckAvailable.html', {})
            else:
                return render(request, 'ProjectCheckUsed.html', {})

def addproject(request):
    try:
        id_token = request.session['TokenID']
        layers = request.POST.get('layers')
        projectid = request.POST.get('projectid')
        neurons = request.POST.get('neurons')
    except:
        return Http404()
    GoogleID = "867858739826-0j8s1vplsccuqcha9tng77pmrpc49mam.apps.googleusercontent.com"
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=" + id_token
    response = requests.get(url)
    if response.json()['iss'] in ('accounts.google.com', 'https://accounts.google.com'):
        if response.json()['aud'] == GoogleID:
            # response['auth'] = os.environ['password']
            userid = response.json()['sub']
            post_data = {'auth': os.environ['password'], 'projectid': projectid}
            response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getProjectInfo', data=post_data)
            if (response.json()['message'] == 'could not get project info'):
                key = ''.join(random.choice(string.lowercase) for i in range(20))
                salt = bcrypt.gensalt()
                apikey = bcrypt.hashpw(key,salt)
                post_data = {'auth': os.environ['password'], 'projectid': projectid, 'numlayers': layers, 'nodes': neurons,
                         'uid': userid, 'apikey': apikey}
                response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/createNewProject', data=post_data)
                return HttpResponse(json.dumps({'message': response.json()['message']}), content_type='application/json')
            """
            if (response.json()['message'] == 'could not get project info'):
                post_data = {'auth': os.environ['password'], 'uid': userid}
                response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getUserProjects',data=post_data)
                try:
                    Projects = response.json()['project_list'].split()
                except:
                    Projects = ['']
                ProjectNumber = len(Projects)
                ProjectList = ['' for x in range(ProjectNumber)]
                Neurons = ['' for x in range(ProjectNumber)]
                NeuronLength = ['' for x in range(ProjectNumber)]
                for x in range(ProjectNumber):
                    if (x != 0):
                        post_data = {'auth': os.environ['password'], 'projectid': Projects[x]}
                        response = requests.post(
                            'https://echelon-nn.herokuapp.com/admin/userops/getProjectInfo',data=post_data)
                        ProjectList[x] = response.json()
                        ProjectList[x]['Neurons_per_Layer'] = response.json()['Neurons_per_Layer'].split(',')
                        ProjectList[x]['NeuronLength'] = len(response.json()['Neurons_per_Layer'].split(','))
                        ProjectList.pop(0)
                        return render(request, 'Example.html', {'Projects': ProjectList, 'ProjectID': projectid})
    """


def deleteproject(request):
    try:
        id_token = request.session['TokenID']
        projectid = request.POST.get('projectid')
    except:
        return Http404()
    GoogleID = "867858739826-0j8s1vplsccuqcha9tng77pmrpc49mam.apps.googleusercontent.com"
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=" + id_token
    response = requests.get(url)
    if response.json()['iss'] in ('accounts.google.com', 'https://accounts.google.com'):
        if response.json()['aud'] == GoogleID:
            # response['auth'] = os.environ['password']
            userid = response.json()['sub']
            post_data = {'auth': os.environ['password'], 'projectid': projectid}
            response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/deleteProject', data=post_data)
            post_data = {'auth': os.environ['password'], 'uid': userid}
            response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getUserProjects', data=post_data)
            try:
                Projects = response.json()['project_list'].split()
            except:
                Projects = ['']
            ProjectNumber = len(Projects)
            ProjectList = ['' for x in range(ProjectNumber)]
            Neurons = ['' for x in range(ProjectNumber)]
            NeuronLength = ['' for x in range(ProjectNumber)]
            for x in range(ProjectNumber):
                if (x != 0):
                    post_data = {'auth': os.environ['password'], 'projectid': Projects[x]}
                    response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getProjectInfo',
                                             data=post_data)
                    ProjectList[x] = response.json()
                    ProjectList[x]['Neurons_per_Layer'] = response.json()['Neurons_per_Layer'].split(',')
                    ProjectList[x]['NeuronLength'] = len(response.json()['Neurons_per_Layer'].split(','))
            ProjectList.pop(0)
            return render(request, 'Example.html', {'Projects': ProjectList,'ProjectID':projectid})

def editproject(request):
    try:
        id_token = request.session['TokenID']
        layers = request.POST.get('layers')
        projectid = request.POST.get('projectid')
        neurons = request.POST.get('neurons')
    except:
        return Http404()
    GoogleID = "867858739826-0j8s1vplsccuqcha9tng77pmrpc49mam.apps.googleusercontent.com"
    url = "https://www.googleapis.com/oauth2/v3/tokeninfo?id_token=" + id_token
    response = requests.get(url)
    if response.json()['iss'] in ('accounts.google.com', 'https://accounts.google.com'):
        if response.json()['aud'] == GoogleID:
            # response['auth'] = os.environ['password']
            userid = response.json()['sub']
            post_data = {'auth': os.environ['password'], 'projectid': projectid, 'numlayers':layers, 'nodes':neurons}
            response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/editProject', data=post_data)
            post_data = {'auth': os.environ['password'], 'uid': userid}
            response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getUserProjects', data=post_data)
            try:
                Projects = response.json()['project_list'].split()
                ProjectNumber = len(Projects)
                ProjectList = ['' for x in range(ProjectNumber)]
                Neurons = ['' for x in range(ProjectNumber)]
                NeuronLength = ['' for x in range(ProjectNumber)]
                for x in range(ProjectNumber):
                    if (x != 0):
                        post_data = {'auth': os.environ['password'], 'projectid': Projects[x]}
                        response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getProjectInfo',
                                                 data=post_data)
                        ProjectList[x] = response.json()
                        ProjectList[x]['Neurons_per_Layer'] = response.json()['Neurons_per_Layer'].split(',')
                        ProjectList[x]['NeuronLength'] = len(response.json()['Neurons_per_Layer'].split(','))
                ProjectList.pop(0)
                return render(request, 'Example.html',
                              {'Projects': ProjectList, 'ProjectID': projectid, 'Number': ProjectNumber})
            except:
                Projects = ['']
                return HttpResponse('<b>ayyo</b>', content_type='application/html')
    #return HttpResponse(json.dumps('nahhhh'), content_type='application/json')

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
            userid = response.json()['sub']
            post_data = {'auth': os.environ['password'], 'uid': userid}
            response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getUserData', data=post_data)
            if response.json()['error'] == "NA":
                UserCredits = response.json()['credits']
                return render(request, 'tracker/Credits.html', {'Credits':UserCredits})

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
            return render(request, 'tracker/Faliure.html', {'JSON': response.json()})
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
                try:
                    Projects = response.json()['project_list'].split()
                    ProjectNumber = len(Projects)
                    ProjectList = ['' for x in range(ProjectNumber)]
                    Neurons = ['' for x in range(ProjectNumber)]
                    NeuronLength = ['' for x in range(ProjectNumber)]
                except:
                    Projects = ['']
                    ProjectNumber = len(Projects)
                    ProjectList = ['' for x in range(ProjectNumber)]
                    #return HttpResponse(json.dumps({'message': response.json()['error']}),
                     #                   content_type='application/json')
                for x in range(ProjectNumber):
                    if (x != 0):
                        post_data = {'auth': os.environ['password'], 'projectid': Projects[x]}
                        response = requests.post('https://echelon-nn.herokuapp.com/admin/userops/getProjectInfo',
                                                 data=post_data)
                        ProjectList[x]['Project_ID'] = response.json()['Project_ID']
                        ProjectList[x]['Neurons_per_Layer'] = response.json()['Neurons_per_Layer'].split(',')
                        ProjectList[x]['NeuronLength'] = len(response.json()['Neurons_per_Layer'].split(','))
                ProjectList.pop(0)
                return render(request, 'tracker/Projects.html',
                              {'Projects': ProjectList, 'UserName': UserName, 'number': ProjectNumber})
            else:
                return render(request, 'tracker/Projects.html', {'JSON':response.json()['error']})
        else:
            return render(request, 'tracker/Faliure.html', {})
    else:
        return render(request, 'tracker/UserPortal.html', {})