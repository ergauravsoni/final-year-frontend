from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.views.static import serve
import os
import requests
from datetime import datetime, timedelta
from pathlib import Path

ENDPOINT_URL = 'https://b5684f2f9a15.ngrok.io/api/'
BASE_DIR = Path(__file__).resolve().parent.parent


def download(request):
    try:
        r = requests.get(ENDPOINT_URL + 'users/me/',headers=request.session['auth_payload'])
        print(r.json())
        print(r.status_code)
        if r.status_code >= 200 and r.status_code < 300:
            r2 = requests.get(ENDPOINT_URL + 'games/score_list/',headers=request.session['auth_payload'])
            print(r2.json())
            content = {'email': r.json()['email'],'name': r.json()['name']}
            file = open("file.txt", "w")
 
            #convert variable to string
            str1 = repr(r.json())
            str2 = repr(r2.json())
            str3 = ""

            content ={}

            if r2.json()[0]['inventory_score']==0:
                str3 = "Unable to evaluate. Try Again."
            elif r2.json()[0]['inventory_score']>0 and r2.json()[0]['inventory_score']<11:
                str3 = "These ups and downs are considered normal."
            elif r2.json()[0]['inventory_score']>10 and r2.json()[0]['inventory_score']<17:
                str3 = "Mild Mood Disturbance"
            elif r2.json()[0]['inventory_score']>16 and r2.json()[0]['inventory_score']<21:
                str3 = "Borderline Clinical Depression"
            elif r2.json()[0]['inventory_score']>20 and r2.json()[0]['inventory_score']<31:
                str3 = "Moderate Depression"
            elif r2.json()[0]['inventory_score']>30 and r2.json()[0]['inventory_score']<41:
                str3 = "Severe Depression"
            else:
                str3 = "Extreme Depression"
            
            if r2.json()[0]['tower_blocks_score']>40:
                content['tb_score_factor'] = 'High'
                content['tb_color'] = 'success'
            elif r2.json()[0]['tower_blocks_score']<21:
                content['tb_score_factor'] = 'Low'
                content['tb_color'] = 'danger'
            else:
                content['tb_score_factor'] = 'Average'
                content['tb_color'] = 'warning'
            
            content['bounce_score'] = r2.json()[0]['bounce_score']
            if r2.json()[0]['bounce_score']<41:
                content['b_score_factor'] = 'High'
                content['b_color'] = 'success'
            elif r2.json()[0]['bounce_score']>50:
                content['b_score_factor'] = 'Low'
                content['b_color'] = 'danger'
            else:
                content['b_score_factor'] = 'Average'
                content['b_color'] = 'warning'
            
            content['kill_birds_score'] = r2.json()[0]['kill_birds_score']
            if r2.json()[0]['kill_birds_score']>4:
                content['kb_score_factor'] = 'High'
                content['kb_color'] = 'success'
            elif r2.json()[0]['kill_birds_score']<3:
                content['kb_score_factor'] = 'Low'
                content['kb_color'] = 'danger'
            else:
                content['kb_score_factor'] = 'Average'
                content['kb_color'] = 'warning'
            
            content['snake_score'] = r2.json()[0]['snake_score']
            if r2.json()[0]['snake_score']>14:
                content['s_score_factor'] = 'High'
                content['s_color'] = 'success'
            elif r2.json()[0]['snake_score']<5:
                content['s_score_factor'] = 'Low'
                content['s_color'] = 'danger'
            else:
                content['s_score_factor'] = 'Average'
                content['s_color'] = 'warning'

            tbn=0
            if content['tb_score_factor']=='High':
                tbn=3
            elif content['tb_score_factor']=='Average':
                tbn=2
            else:
                tbn=1

            bn=0
            if content['b_score_factor']=='High':
                bn=3
            elif content['b_score_factor']=='Average':
                bn=2
            else:
                bn=1

            kbn=0
            if content['kb_score_factor']=='High':
                kbn=3
            elif content['kb_score_factor']=='Average':
                kbn=2
            else:
                kbn=1

            sn=0
            if content['s_score_factor']=='High':
                sn=3
            elif content['s_score_factor']=='Average':
                sn=2
            else:
                sn=1

            content['perception_percent'] = str(round(23.33*tbn + 10*kbn))
            content['attention_percent'] = str(round(20*sn + 13.33*bn))
            content['learning_percent'] = str(round(33.33*sn))

            str4 = "Perception = " + content['perception_percent'] + "% \n" + "Attention = " + content['attention_percent'] + "%\nLearning = " + content['learning_percent'] + "%\n"
            
            r3 = requests.get("https://thingspeak.com/channels/1408511/fields/3/last.json?api_key=0IQJRAN4L6IQO10B")
            print("BPM:",r3.json())
            str5 = r3.json()['field3']
            
            r4 = requests.get("https://thingspeak.com/channels/1408511/fields/1/last.json?api_key=0IQJRAN4L6IQO10B")
            print("Steps:",r4.json())
            str6 = r4.json()['field1']

            r5 = requests.get("https://thingspeak.com/channels/1408511/fields/2/last.json?api_key=0IQJRAN4L6IQO10B")
            print("Calories:",r5.json())
            str7 = r5.json()['field2']

            file.write("Overall Health Analytical Report\n\nUser Details = " + str1 + "\n\n" + "Game Analytics Report = " + str2 + "\n\n" + "Neuropsychiatric Report :\n" + str4 + "\n" + "Depression Detection Inventory Report = " + str3 + "\n\nHeartrate (BPM) = " + str5 + "\n\nStep Count = " + str6 + "\n\nEnergy Consumed(Calories) = " + str7)
            #close file
            file.close()

            filepath = str(BASE_DIR) + "/file.txt"
            return serve(request, os.path.basename(filepath), os.path.dirname(filepath))
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('users:signin'))

def dashboard(request):
    try:
        r = requests.get(ENDPOINT_URL + 'users/me/',headers=request.session['auth_payload'])
        print(r.json())
        print(r.status_code)
        if r.status_code >= 200 and r.status_code < 300:
            content = {'email': r.json()['email'],'name': r.json()['name']}
            return render(request, "main/dashboard.html",content)
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('users:signin'))

@csrf_exempt
def tower_blocks(request):
    if request.method == 'POST':
        print('Tower Blocks Score:',request.POST['score'])
        payload={
            'tower_blocks_score':request.POST['score'],
            'user':request.POST['email']    
        }
        r = requests.put(ENDPOINT_URL + 'games/score_update/',data=payload,headers=request.session['auth_payload'])
        print(r.json())
        print(r.status_code)
        return HttpResponseRedirect(reverse('main:dashboard'))
    else:
        try:
            r = requests.get(ENDPOINT_URL + 'users/me/',headers=request.session['auth_payload'])
            print(r.json())
            print(r.status_code)
            if r.status_code >= 200 and r.status_code < 300:
                content = {'email': r.json()['email'],'name': r.json()['name']}
                return render(request, "main/tower_blocks.html",content)
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('users:signin'))

@csrf_exempt
def bounce(request):
    if request.method == 'POST':
        print('Bounce Score:',request.POST['score'])
        payload={
            'bounce_score':request.POST['score'],
            'user':request.POST['email']    
        }
        r = requests.put(ENDPOINT_URL + 'games/score_update/',data=payload,headers=request.session['auth_payload'])
        print(r.json())
        print(r.status_code)
        return HttpResponseRedirect(reverse('main:dashboard'))
    else:
        try:
            r = requests.get(ENDPOINT_URL + 'users/me/',headers=request.session['auth_payload'])
            print(r.json())
            print(r.status_code)
            if r.status_code >= 200 and r.status_code < 300:
                content = {'email': r.json()['email'],'name': r.json()['name']}
                return render(request, "main/bounce.html",content)
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('users:signin'))

@csrf_exempt
def kill_birds(request):
    if request.method == 'POST':
        print('Kill Birds Score:',request.POST['score'])
        payload={
            'kill_birds_score':request.POST['score'],
            'user':request.POST['email']    
        }
        r = requests.put(ENDPOINT_URL + 'games/score_update/',data=payload,headers=request.session['auth_payload'])
        print(r.json())
        print(r.status_code)
        return HttpResponseRedirect(reverse('main:dashboard'))
    else:
        try:
            r = requests.get(ENDPOINT_URL + 'users/me/',headers=request.session['auth_payload'])
            print(r.json())
            print(r.status_code)
            if r.status_code >= 200 and r.status_code < 300:
                content = {'email': r.json()['email'],'name': r.json()['name']}
                return render(request, "main/kill_birds.html",content)
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('users:signin'))

@csrf_exempt
def snake(request):
    if request.method == 'POST':
        print('Snake Score:',request.POST['score'])
        payload={
            'snake_score':request.POST['score'],
            'user':request.POST['email']    
        }
        r = requests.put(ENDPOINT_URL + 'games/score_update/',data=payload,headers=request.session['auth_payload'])
        print(r.json())
        print(r.status_code)
        return HttpResponseRedirect(reverse('main:dashboard'))
    else:
        try:
            r = requests.get(ENDPOINT_URL + 'users/me/',headers=request.session['auth_payload'])
            print(r.json())
            print(r.status_code)
            if r.status_code >= 200 and r.status_code < 300:
                content = {'email': r.json()['email'],'name': r.json()['name']}
                return render(request, "main/snake.html",content)
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('users:signin'))

def game_analytics(request):
    try:
        r1 = requests.get(ENDPOINT_URL + 'users/me/',headers=request.session['auth_payload'])
        r2 = requests.get(ENDPOINT_URL + 'games/score_list/',headers=request.session['auth_payload'])
        print(r1.json())
        print(r1.status_code)
        print(r2.json())
        print(r2.status_code)
        if r1.status_code >= 200 and r1.status_code < 300:
            content = {'email': r1.json()['email'],'name': r1.json()['name']}
            
            content['tower_blocks_score'] = r2.json()[0]['tower_blocks_score']
            if r2.json()[0]['tower_blocks_score']>40:
                content['tb_score_factor'] = 'High'
                content['tb_color'] = 'success'
            elif r2.json()[0]['tower_blocks_score']<21:
                content['tb_score_factor'] = 'Low'
                content['tb_color'] = 'danger'
            else:
                content['tb_score_factor'] = 'Average'
                content['tb_color'] = 'warning'
            
            content['bounce_score'] = r2.json()[0]['bounce_score']
            if r2.json()[0]['bounce_score']<41:
                content['b_score_factor'] = 'High'
                content['b_color'] = 'success'
            elif r2.json()[0]['bounce_score']>50:
                content['b_score_factor'] = 'Low'
                content['b_color'] = 'danger'
            else:
                content['b_score_factor'] = 'Average'
                content['b_color'] = 'warning'
            
            content['kill_birds_score'] = r2.json()[0]['kill_birds_score']
            if r2.json()[0]['kill_birds_score']>4:
                content['kb_score_factor'] = 'High'
                content['kb_color'] = 'success'
            elif r2.json()[0]['kill_birds_score']<3:
                content['kb_score_factor'] = 'Low'
                content['kb_color'] = 'danger'
            else:
                content['kb_score_factor'] = 'Average'
                content['kb_color'] = 'warning'
            
            content['snake_score'] = r2.json()[0]['snake_score']
            if r2.json()[0]['snake_score']>14:
                content['s_score_factor'] = 'High'
                content['s_color'] = 'success'
            elif r2.json()[0]['snake_score']<5:
                content['s_score_factor'] = 'Low'
                content['s_color'] = 'danger'
            else:
                content['s_score_factor'] = 'Average'
                content['s_color'] = 'warning'

            tbn=0
            if content['tb_score_factor']=='High':
                tbn=3
            elif content['tb_score_factor']=='Average':
                tbn=2
            else:
                tbn=1

            bn=0
            if content['b_score_factor']=='High':
                bn=3
            elif content['b_score_factor']=='Average':
                bn=2
            else:
                bn=1

            kbn=0
            if content['kb_score_factor']=='High':
                kbn=3
            elif content['kb_score_factor']=='Average':
                kbn=2
            else:
                kbn=1

            sn=0
            if content['s_score_factor']=='High':
                sn=3
            elif content['s_score_factor']=='Average':
                sn=2
            else:
                sn=1

            content['perception_percent'] = round(23.33*tbn + 10*kbn)
            content['attention_percent'] = round(20*sn + 13.33*bn)
            content['learning_percent'] = round(33.33*sn)
    
            date_obj = datetime.fromisoformat(r2.json()[0]['last_updated'])
            print(date_obj.tzinfo,date_obj.microsecond)
            date_p = datetime.fromisoformat((date_obj.strftime("%Y-%m-%d %H:%M:%S")))
            print(date_p)
            print(date_p+timedelta(hours=3,minutes=30,microseconds=int(date_obj.microsecond)))
            date_f=date_p+timedelta(hours=3,minutes=30,microseconds=int(date_obj.microsecond))
            content['last_updated'] = date_f
            

            return render(request, "main/game_analytics.html",content)
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('users:signin'))

@csrf_exempt
def inventory(request):
    if request.method == 'POST':
        print('Inventory Score:',request.POST['score'])
        payload={
            'inventory_score':request.POST['score'],
            'user':request.POST['email']    
        }
        r = requests.put(ENDPOINT_URL + 'games/score_update/',data=payload,headers=request.session['auth_payload'])
        print(r.json())
        print(r.status_code)
        return HttpResponseRedirect(reverse('main:dashboard'))
    else:
        try:
            r = requests.get(ENDPOINT_URL + 'users/me/',headers=request.session['auth_payload'])
            print(r.json())
            print(r.status_code)
            if r.status_code >= 200 and r.status_code < 300:
                content = {'email': r.json()['email'],'name': r.json()['name']}
                return render(request, "main/inventory.html",content)
        except KeyError:
            pass
        return HttpResponseRedirect(reverse('users:signin'))    
