from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

import requests

ENDPOINT_URL = 'https://65f1399fb0fe.ngrok.io/api/users/'

def dashboard(request):
    try:
        r = requests.get(ENDPOINT_URL + 'me/',headers=request.session['auth_payload'])
        print(r.json())
        print(r.status_code)
        if r.status_code >= 200 and r.status_code < 300:
            content = {'email': r.json()['email'],'name': r.json()['name']}
            return render(request, "main/dashboard.html",content)
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('users:signin'))
