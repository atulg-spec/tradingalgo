from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
import json
import requests
from alerts.models import *
from threading import Thread

# Create your views here.
@login_required
@permission_required('is_superuser')
@user_passes_test(lambda u: u.is_superuser)
def place_alert(request, id):
    thread = Thread(target=Placed,args=(request,id))
    thread.start()
    messages.success(request,'Alert Placed Successfully !')
    return redirect('/admin/alerts/orders/')


def Placed(request,id):
    f = open("alerting.txt", "a")
    f.write(f'POSITION \n')
    f.close()
    try:
        print(2)
        ord = orders.objects.filter(id=id).first()
        print(3)
        try:
            print(4)
            data = json.loads(json.dumps(ord.syntax))
            url = f'https://smart-algo.in/alert/{ord.webhook.url}'
            f = open("alerting.txt", "a")
            f.write(f'{url} \n')
            f.close()
            response = requests.post(url,data)
            print(5)
            print(6)
            f = open("alerting.txt", "a")
            f.write(f'{response.status_code} \n')
            f.close()
            messages.success(request,'Alert Placed Successfully !')
        except Exception as e:
            print(7)
            print(e)
            messages.error(request,f'Oops ! Alert Failed {e}')
            ord.status = 'failed'
            ord.save()
    except:
        messages.error(request,f'Alert failed ! {e}')
