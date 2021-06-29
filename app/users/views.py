from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

import requests

ENDPOINT_URL = 'https://65f1399fb0fe.ngrok.io/api/users/'

def profile(request):
    message=""
    if request.method == 'POST':
        payload = {'email': request.POST['email'], 'password': request.POST['password'], 'name': request.POST['name']}
        r = requests.put(ENDPOINT_URL + 'me/',data=payload,headers=request.session['auth_payload'])
        print(r.json())
        print(r.status_code)
        if r.status_code >= 200 and r.status_code < 300:
            message="Success"
        else:
            message="Bad Request"    
        try:
            r = requests.get(ENDPOINT_URL + 'me/',headers=request.session['auth_payload'])
            print(r.json())
            print(r.status_code)
            if r.status_code >= 200 and r.status_code < 300:
                context = {
                    'email': r.json()['email'],
                    'name': r.json()['name'],
                    'message': message,
                }
                return render(request, "users/profile.html",context)
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('users:signin'))
    else:
        try:
            r = requests.get(ENDPOINT_URL + 'me/',headers=request.session['auth_payload'])
            print(r.json())
            print(r.status_code)
            if r.status_code >= 200 and r.status_code < 300:
                content = {
                    'email': r.json()['email'],
                    'name': r.json()['name'],
                    'message': message,
                }
                return render(request, "users/profile.html",content)
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('users:signin'))

def signup(request):
    message=""
    if request.method == 'POST':
        payload = {'email': request.POST['email'], 'password': request.POST['password'], 'name': request.POST['name']}
        r = requests.post(ENDPOINT_URL + 'create/',data=payload)
        print(r.json())
        print(r.status_code)
        if r.status_code >= 200 and r.status_code < 300:
            payload = {'email': request.POST['email'], 'password': request.POST['password']}
            r = requests.post(ENDPOINT_URL + 'token/',data=payload)
            print(r.json())
            print(r.status_code)
            if r.status_code >= 200 and r.status_code < 300:
                request.session['auth_payload'] = {'Authorization': 'token ' + r.json()['token']}
            return HttpResponseRedirect(reverse('main:dashboard'))
        message = "Email Already Exists Or Bad Credentials! Try Again."
    return render(request, "users/sign-up.html",{'message':message})

def signin(request):
    message=""
    if request.method == 'POST':
        payload = {'email': request.POST['email'], 'password': request.POST['password']}
        r = requests.post(ENDPOINT_URL + 'token/',data=payload)
        print(r.json())
        print(r.status_code)
        if r.status_code >= 200 and r.status_code < 300:
            request.session['auth_payload'] = {'Authorization': 'token ' + r.json()['token']}
            return HttpResponseRedirect(reverse('main:dashboard'))
        message = "Bad Credentials! Try Again."
    return render(request, "users/sign-in.html",{'message':message})

def signout(request):
    try:
        del request.session['auth_payload']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('users:signin'))

