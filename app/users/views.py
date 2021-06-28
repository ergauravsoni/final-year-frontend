from django.shortcuts import render
from django.http import HttpResponse

from time import sleep

import requests

def signin(request):
    if request.method == 'POST':
        payload = {'email': request.POST['email'], 'password': request.POST['password']}
        r = requests.post('https://fc28949074b0.ngrok.io/api/users/token/',data=payload)
        print(r.json())
        print(r.status_code)
        if r.status_code >= 200 and r.status_code < 300:
            return HttpResponse('Yay, it worked')
        return HttpResponse('Could not save data')
    else:
        return render(request, "users/sign-in.html")
