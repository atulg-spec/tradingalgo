from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from django.http import HttpResponse
import json
from datetime import datetime,timedelta
import pyotp
from fyers_api import accessToken
try:
    from SmartApi import SmartConnect
except:
    from smartapi import smartConnect
from fyers_api import fyersModel
from dhanhq import dhanhq
from py5paisa import FivePaisaClient
from fyers_api import accessToken
from pya3 import *
from django.views.decorators.csrf import csrf_exempt
from .forms import LoginForm
import random
import string
from trade.notifications.notify_alert import notify_admin
from trade.checksm import RechPayChecksum
from trade.alerts.dhan import dhan_order
from trade.alerts.angel import angel_order
from trade.alerts.paisa import paisa_order
from trade.alerts.alice import alice_order
from trade.alerts.fyers import fyers_order
from trade.alerts.webhook import *
from trade.alerts.limitorders import palce_limit_order
from trade.alerts.getsymbols import symbol_list,get_symbol,avg_price,exc_symbols
from alerts.models import IndexTokens
from django.db.models import Q
User = get_user_model()
al = User.objects.get(username='all')
# SYMBOL LIST
search_symbollist = {}
symboldata = exc_symbols()
for i in symboldata:
    temp = {'symbol':i,'segment':symboldata[i]['exchange'],'token':symboldata[i]['token']}
    search_symbollist[i] = temp
search_symbollist = json.dumps(search_symbollist)
# END SYMBOL LIST


symbollist = symbol_list()

# ORDERID GENERATOR
def orderid(length=15):
    characters = string.ascii_letters + string.digits
    attempts = 0
    while True:
        orderid = ''.join(random.choice(characters) for _ in range(length))
        if not allplan.objects.filter(order_id=orderid).exists():
            return orderid
        attempts += 1


# USER CREATION LOGIN AND SIGNUP
def index(request):
    return render(request,'home.html')

def handlelogout(request):
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect('/login')

# ---------------DASHBOARD
@login_required
def dashboard(request):
    userr = request.user
    angelapiob = angelapi.objects.filter(apiuser=userr)
    paisaapiob = paisaapi.objects.filter(apiuser=userr)
    dhanapiob = dhanapi.objects.filter(apiuser=userr)
    fyersapiapiob = fyersapi.objects.filter(apiuser=userr)
    aliceapiob = aliceapi.objects.filter(apiuser=userr)
    st = allstratergy.objects.filter(user=request.user)
    ob=allstratergy.objects.all()
    ptype = producttype.objects.all()
    otype = ordertype.objects.all()
    seg = segment.objects.all()
    stra = strategy.objects.all()
    headline = news.objects.all()
    try:
        ex = allplan.objects.filter(user=request.user).filter(active=True).first()
        today = timezone.now().date()
        if ex.expiry_date.date() == today:
            ex.delete()
            messages.warning(request,"Your Plan has been expired today. Update Now")
    except:
        pass
    notification = Notifications.objects.filter(Q(user=request.user) | Q(user=al))
    not_seen = Notifications.objects.filter(Q(user=request.user) | Q(user=al)).filter(seen=False).__len__()
    context = {
        "angelapiob":angelapiob,
        "paisaapiob":paisaapiob,
        "dhanapiob":dhanapiob,
        "fyersapiob":fyersapiapiob,
        "aliceapiob":aliceapiob,
        "st":st,
        "ob":ob,
        "ptype":ptype,
        "otype":otype,
        "seg":seg,
        "stra":stra,
        "headline":headline,
        "notification":notification,
        "not_seen":not_seen
        }
    return render(request,'dashboard.html',context)

@login_required
def notify(request):
    notification = Notifications.objects.filter(Q(user=request.user) | Q(user=al))
    for x in notification:
        x.seen = True
        x.save()
    not_seen = Notifications.objects.filter(Q(user=request.user) | Q(user=al)).filter(seen=False).__len__()
    context = {
        "notification":notification,
        "not_seen":not_seen
        }
    return render(request,'notify.html',context)

@login_required
def profile(request):
    if request.method == "POST":
        try:
            qty = bot_order_quantity.objects.filter(user=request.user).first()
            qty.quantity = request.POST.get("quantity")
            qty.crudeoil_quantity = request.POST.get("crudeoil_quantity")
            qty.nifty_quantity = request.POST.get("nifty_quantity")
            qty.bank_nifty_quantity = request.POST.get("bank_nifty_quantity")
            qty.fin_nifty_quantity = request.POST.get("fin_nifty_quantity")
            qty.sensex_quantity = request.POST.get("sensex_quantity")
            qty.bankex_quantity = request.POST.get("bankex_quantity")
            qty.save()
        except:
            qtyob = bot_order_quantity(user=request.user,quantity=request.POST.get("quantity"))
            qtyob.save()
        messages.success(request,"Profile Updated Successfully !")
        return redirect("/profile")
    else:
        notification = Notifications.objects.filter(Q(user=request.user) | Q(user=al))
        not_seen = Notifications.objects.filter(Q(user=request.user) | Q(user=al)).filter(seen=False).__len__()
        userr = request.user
        apiob = fyersapi.objects.filter(apiuser=userr)
        sus = allplan.objects.filter(user=request.user).filter(active=True).first()
        qty = bot_order_quantity.objects.filter(user=request.user).first()
        return render(request,'profile.html',{"userr":userr,"apiob":apiob,"sus":sus,"qty":qty,"notification":notification,"not_seen":not_seen})

@login_required
def apiinfo(request):
    userr = request.user
    angelapiob = angelapi.objects.filter(apiuser=userr)
    return render(request,'api.html',{"angelapiob":angelapiob})

def handlelogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Successfully')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


# ---------------ANGEL API
@login_required
def createangelapi(request):
    #  Suscription Check
    try:
        ex = allplan.objects.filter(user=request.user).filter(active=True).first()
        today = timezone.now().date()
        if ex.expiry_date.date() == today:
            ex.delete()
            messages.warning(request,"Your Plan has been expired today. Update Now")
    except:
        pass
    angelob = angelapi.objects.filter(apiuser=request.user)
    dhanob = dhanapi.objects.filter(apiuser=request.user)
    aliceob = aliceapi.objects.filter(apiuser=request.user)
    paisaob = paisaapi.objects.filter(apiuser=request.user)
    fyersob = fyersapi.objects.filter(apiuser=request.user)
    tlen = angelob.__len__()+dhanob.__len__()+aliceob.__len__()+paisaob.__len__()+fyersob.__len__()
    person = allplan.objects.filter(user=request.user).filter(active=True).first()
    try:
        if person.plan_type == "Basic" or person.plan_type == "Pro" or person.plan_type == "Free":
            if tlen >= 1:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "VIP":
            if tlen >= 2:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "Premium":
            if tlen >= 10:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        else:
            messages.error(request,"Please suscribe to a plan to continue.")
            return redirect("/plan")
    except:
        messages.error(request,"Please suscribe to a plan to continue.")
        return redirect("/plan")
    # Suscription Check Complete
    notification = Notifications.objects.filter(Q(user=request.user) | Q(user=al))
    not_seen = Notifications.objects.filter(Q(user=request.user) | Q(user=al)).filter(seen=False).__len__()
    return render(request,"createangelapi.html",{"notification":notification,"not_seen":not_seen})

@login_required
def saveangelapi(request):
    #  Suscription Check
    try:
        ex = allplan.objects.filter(user=request.user).filter(active=True).first()
        today = timezone.now().date()
        if ex.expiry_date.date() == today:
            ex.delete()
            messages.warning(request,"Your Plan has been expired today. Update Now")
    except:
        pass
    angelob = angelapi.objects.filter(apiuser=request.user)
    dhanob = dhanapi.objects.filter(apiuser=request.user)
    aliceob = aliceapi.objects.filter(apiuser=request.user)
    paisaob = paisaapi.objects.filter(apiuser=request.user)
    fyersob = fyersapi.objects.filter(apiuser=request.user)
    tlen = angelob.__len__()+dhanob.__len__()+aliceob.__len__()+paisaob.__len__()+fyersob.__len__()
    person = allplan.objects.filter(user=request.user).filter(active=True).first()
    try:
        if person.plan_type == "Basic" or person.plan_type == "Pro" or person.plan_type == "Free":
            if tlen >= 1:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "VIP":
            if tlen >= 2:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "Premium":
            if tlen >= 10:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        else:
            messages.error(request,"Please suscribe to a plan to continue.")
            return redirect("/plan")
    except:
        messages.error(request,"Please suscribe to a plan to continue.")
        return redirect("/plan")
    # Suscription Check Complete
    if request.method == "POST":
        try:
            userr = request.user
            name = request.POST.get("name")
            clientid = request.POST.get("clientid")
            password = request.POST.get("password")
            apikey = request.POST.get("apikey")
            totp = request.POST.get("totp")
            obj=SmartConnect(api_key= apikey)
            data = obj.generateSession(clientid,password,totp)
            rtoken= data['data']['refreshToken']
            authtoken= data['data']['jwtToken']
            authtoken=authtoken.replace("Bearer ", "")
            apiob = angelapi(apiuser=userr,apiname=name,clientid=clientid,password=password,apikey=apikey,totp=totp,rtoken=rtoken,authtoken=authtoken)
            apiob.save()
            messages.success(request,"ANGEL API Created Successfully.")
            return redirect("/dashboard")
        except Exception as e:
            messages.error(request,"Invalid Credentials")
            return redirect('/createangelapi')
    else:
        return redirect("/dashboard")

@login_required
def modifyangel(request,apiid):
    current_api = angelapi.objects.filter(apiid = apiid).first()
    if current_api.apiuser != request.user:
        return redirect('/')
    if request.method == "POST":
        try:
            userr = request.user
            apiname = request.POST.get("name")
            clientid = request.POST.get("clientid")
            password = request.POST.get("password")
            apikey = request.POST.get("apikey")
            totp = request.POST.get("totp")
            obj=SmartConnect(api_key= apikey)
            data = obj.generateSession(clientid,password,totp)
            rtoken= data['data']['refreshToken']
            authtoken= data['data']['jwtToken']
            authtoken=authtoken.replace("Bearer ", "")
            apiob = angelapi(apiid=apiid,apiuser=userr,apiname=apiname,clientid=clientid,password=password,apikey=apikey,totp=totp,rtoken=rtoken,authtoken=authtoken,datetime=datetime.now())
            apiob.save()
            messages.success(request,"Changes applied Successfully.")
            return redirect("/dashboard")
        except Exception as e:
            messages.error(request,"Invalid Credentials")
            return render(request,'modifyangel.html',{"current_api":current_api})
    else:
        return render(request,'modifyangel.html',{"current_api":current_api})

@login_required
def deleteangelapi(request,apiid):
    current_api = angelapi.objects.filter(apiid = apiid).first()
    if current_api.apiuser != request.user:
        return redirect('/')
    delete=angelapi(apiid=apiid)
    delete.delete()
    messages.success(request,"API deleted successfully")
    return redirect("/dashboard")

# -------------DHAN API
@login_required
def createdhanapi(request):
    #  Suscription Check
    try:
        ex = allplan.objects.filter(user=request.user).filter(active=True).first()
        today = timezone.now().date()
        if ex.expiry_date.date() == today:
            ex.delete()
            messages.warning(request,"Your Plan has been expired today. Update Now")
    except:
        pass
    angelob = angelapi.objects.filter(apiuser=request.user)
    dhanob = dhanapi.objects.filter(apiuser=request.user)
    aliceob = aliceapi.objects.filter(apiuser=request.user)
    paisaob = paisaapi.objects.filter(apiuser=request.user)
    fyersob = fyersapi.objects.filter(apiuser=request.user)
    tlen = angelob.__len__()+dhanob.__len__()+aliceob.__len__()+paisaob.__len__()+fyersob.__len__()
    person = allplan.objects.filter(user=request.user).filter(active=True).first()
    try:
        if person.plan_type == "Basic" or person.plan_type == "Pro" or person.plan_type == "Free":
            if tlen >= 1:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "VIP":
            if tlen >= 2:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "Premium":
            if tlen >= 10:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        else:
            messages.error(request,"Please suscribe to a plan to continue.")
            return redirect("/plan")
    except:
        messages.error(request,"Please suscribe to a plan to continue.")
        return redirect("/plan")
    # Suscription Check Complete
    if request.method == "POST":
        try:
            userr = request.user
            name = request.POST.get("name")
            clientid = request.POST.get("clientid")
            accesstoken = request.POST.get("accesstoken")
            dhan = dhanhq(clientid,accesstoken)
            apiob = dhanapi(apiuser=userr,apiname=name,clientid=clientid,accesstoken=accesstoken)
            apiob.save()
            messages.success(request,"DHANHQ Api Created Successfully.")
            return redirect("/dashboard")
        except Exception as e:
            messages.error(request,f"INVALID CREADENTIALS")
            return redirect('/createdhanapi')
    else:
        return render(request,"createdhanapi.html")

@login_required
def modifydhanapi(request,apiid):
    current_api = dhanapi.objects.filter(apiid = apiid).first()
    if current_api.apiuser != request.user:
        return redirect('/')
    if request.method == "POST":
        userr = request.user
        apiname = request.POST.get("name")
        clientid = request.POST.get("clientid")
        accesstoken = request.POST.get("accesstoken")
        apiob = dhanapi(apiid=apiid,apiuser=userr,apiname=apiname,clientid=clientid,accesstoken=accesstoken,datetime=datetime.now())
        apiob.save()
        messages.success(request,"Changes applied Successfully.")
        return redirect("/dashboard")
    else:
        return render(request,'modifydhan.html',{"current_api":current_api})

@login_required
def deletedhanapi(request,apiid):
    current_api = dhanapi.objects.filter(apiid = apiid).first()
    if current_api.apiuser != request.user:
        return redirect('/')
    delete=dhanapi(apiid=apiid)
    delete.delete()
    messages.success(request,"API deleted successfully")
    return redirect("/dashboard")


# ------------ALICE BLUE API
@login_required
def createaliceapi(request):
    #  Suscription Check
    try:
        ex = allplan.objects.filter(user=request.user).filter(active=True).first()
        today = timezone.now().date()
        if ex.expiry_date.date() == today:
            ex.delete()
            messages.warning(request,"Your Plan has been expired today. Update Now")
    except:
        pass
    angelob = angelapi.objects.filter(apiuser=request.user)
    dhanob = dhanapi.objects.filter(apiuser=request.user)
    aliceob = aliceapi.objects.filter(apiuser=request.user)
    paisaob = paisaapi.objects.filter(apiuser=request.user)
    fyersob = fyersapi.objects.filter(apiuser=request.user)
    tlen = angelob.__len__()+dhanob.__len__()+aliceob.__len__()+paisaob.__len__()+fyersob.__len__()
    person = allplan.objects.filter(user=request.user).filter(active=True).first()
    try:
        if person.plan_type == "Basic" or person.plan_type == "Pro" or person.plan_type == "Free":
            if tlen >= 1:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "VIP":
            if tlen >= 2:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "Premium":
            if tlen >= 10:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        else:
            messages.error(request,"Please suscribe to a plan to continue.")
            return redirect("/plan")
    except:
        messages.error(request,"Please suscribe to a plan to continue.")
        return redirect("/plan")
    # Suscription Check Complete
    if request.method == "POST":
        try:
            userr = request.user
            name = request.POST.get("name")
            userid = request.POST.get("userid")
            apikey = request.POST.get("apikey")
            alice = Aliceblue(user_id=userid,api_key=apikey)
            id = alice.get_session_id()
            order = id["sessionID"]
            apiob = aliceapi(apiuser=userr,apiname=name,userid=userid,apikey=apikey)
            apiob.save()
            messages.success(request,"ALICE BLUE Api Created Successfully.")
            return redirect("/dashboard")
        except Exception as e:
            f = open("aliceerror.txt", "a")
            f.write(f'yahi error hai, {e} \n')
            f.close()
            messages.error(request,"Invalid Credentials")
            return redirect('/createaliceapi')
    else:
        return render(request,"createaliceapi.html")

@login_required
def modifyaliceapi(request,apiid):
    current_api = aliceapi.objects.filter(apiid = apiid).first()
    if current_api.apiuser != request.user:
        return redirect('/')
    if request.method == "POST":
        try:
            userr = request.user
            apiname = request.POST.get("name")
            userid = request.POST.get("userid")
            apikey = request.POST.get("apikey")
            alice = Aliceblue(user_id=userid,api_key=apikey)
            id = alice.get_session_id()
            order = id["sessionID"]
            apiob = aliceapi(apiid=apiid,apiuser=userr,apiname=apiname,userid=userid,apikey=apikey,datetime=datetime.now())
            apiob.save()
            messages.success(request,"Changes applied Successfully.")
            return redirect("/dashboard")
        except Exception as e:
            messages.error(request,"Invalid Credentials")
            return render(request,'modifyalice.html',{"current_api":current_api})
    else:
        return render(request,'modifyalice.html',{"current_api":current_api})

@login_required
def deletealiceapi(request,apiid):
    current_api = aliceapi.objects.filter(apiid = apiid).first()
    if current_api.apiuser != request.user:
        return redirect('/')
    delete=aliceapi(apiid=apiid)
    delete.delete()
    messages.success(request,"API deleted successfully")
    return redirect("/dashboard")

# ----------5PAISA API
@login_required
def createpaisaapi(request):
    #  Suscription Check
    try:
        ex = allplan.objects.filter(user=request.user).filter(active=True).first()
        today = timezone.now().date()
        if ex.expiry_date.date() == today:
            ex.delete()
            messages.warning(request,"Your Plan has been expired today. Update Now")
    except:
        pass
    angelob = angelapi.objects.filter(apiuser=request.user)
    dhanob = dhanapi.objects.filter(apiuser=request.user)
    aliceob = aliceapi.objects.filter(apiuser=request.user)
    paisaob = paisaapi.objects.filter(apiuser=request.user)
    fyersob = fyersapi.objects.filter(apiuser=request.user)
    tlen = angelob.__len__()+dhanob.__len__()+aliceob.__len__()+paisaob.__len__()+fyersob.__len__()
    person = allplan.objects.filter(user=request.user).filter(active=True).first()
    try:
        if person.plan_type == "Basic" or person.plan_type == "Pro" or person.plan_type == "Free":
            if tlen >= 1:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "VIP":
            if tlen >= 2:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "Premium":
            if tlen >= 10:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        else:
            messages.error(request,"Please suscribe to a plan to continue.")
            return redirect("/plan")
    except:
        messages.error(request,"Please suscribe to a plan to continue.")
        return redirect("/plan")
    # Suscription Check Complete
    if request.method == "POST":
        try:
            userr = request.user
            name = request.POST.get("name")
            appsource = request.POST.get("appsource")
            userid = request.POST.get("userid")
            password = request.POST.get("password")
            userkey = request.POST.get("userkey")
            encryptionkey = request.POST.get("encryptionkey")
            secretkey = request.POST.get("secretkey")
            clientcode = request.POST.get("clientcode")
            mpin = request.POST.get("mpin")
            apiob = paisaapi(apiuser=userr,apiname=name,appsource=appsource,userid=userid,password=password,userkey=userkey,encryptionkey=encryptionkey,secretkey=secretkey,clientcode=clientcode,mpin=mpin)
            apiob.save()
            totp = pyotp.TOTP(secretkey, interval=30)
            tcode = totp.now()
            messages.success(request,f"5 PAISA Api Created Successfully.Your TOTP is {tcode}")
            return redirect("/dashboard")
        except Exception as e:
            messages.error(request,f"Invalid Credentials")
            return redirect('/createpaisaapi')
    else:
        return render(request,"createpaisaapi.html")

@login_required
def modifypaisaapi(request,apiid):
    current_api = paisaapi.objects.filter(apiid = apiid).first()
    if current_api.apiuser != request.user:
        return redirect('/')
    if request.method == "POST":
        userr = request.user
        apiname = request.POST.get("name")
        appsource = request.POST.get("appsource")
        userid = request.POST.get("userid")
        password = request.POST.get("password")
        userkey = request.POST.get("userkey")
        encryptionkey = request.POST.get("encryptionkey")
        secretkey = request.POST.get("secretkey")
        clientcode = request.POST.get("clientcode")
        mpin = request.POST.get("mpin")
        apiob = paisaapi(apiid=apiid,apiuser=userr,apiname=apiname,appsource=appsource,userid=userid,password=password,userkey=userkey,encryptionkey=encryptionkey,secretkey=secretkey,clientcode=clientcode,mpin=mpin,datetime=datetime.now())
        apiob.save()
        totp = pyotp.TOTP(secretkey, interval=30)
        tcode = totp.now()
        messages.success(request,f"Changes applied Successfully. Your TOTP is {tcode}")
        return redirect("/dashboard")
    else:
        return render(request,'modifypaisaapi.html',{"current_api":current_api})

def deletepaisaapi(request,apiid):
    current_api = paisaapi.objects.filter(apiid = apiid).first()
    if current_api.apiuser != request.user:
        return redirect('/')
    delete= paisaapi(apiid=apiid)
    delete.delete()
    messages.success(request,"API deleted successfully")
    return redirect("/dashboard")

# ---------------FYERS API
@login_required
def createfyersapi(request):
    #  Suscription Check
    try:
        ex = allplan.objects.filter(user=request.user).filter(active=True).first()
        today = timezone.now().date()
        if ex.expiry_date.date() == today:
            ex.delete()
            messages.warning(request,"Your Plan has been expired today. Update Now")
    except:
        pass
    angelob = angelapi.objects.filter(apiuser=request.user)
    dhanob = dhanapi.objects.filter(apiuser=request.user)
    aliceob = aliceapi.objects.filter(apiuser=request.user)
    paisaob = paisaapi.objects.filter(apiuser=request.user)
    fyersob = fyersapi.objects.filter(apiuser=request.user)
    tlen = angelob.__len__()+dhanob.__len__()+aliceob.__len__()+paisaob.__len__()+fyersob.__len__()
    person = allplan.objects.filter(user=request.user).filter(active=True).first()
    try:
        if person.plan_type == "Basic" or person.plan_type == "Pro" or person.plan_type == "Free":
            if tlen >= 1:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "VIP":
            if tlen >= 2:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        elif person.plan_type == "Premium":
            if tlen >= 10:
                messages.error(request,"Max API limit reached. Please Update your plan to add more.")
                return redirect("/dashboard")
        else:
            messages.error(request,"Please suscribe to a plan to continue.")
            return redirect("/plan")
    except:
        messages.error(request,"Please suscribe to a plan to continue.")
        return redirect("/plan")
    # Suscription Check Complete
    if request.method == "POST":
        try:
            userr = request.user
            name = request.POST.get("name")
            client_id = request.POST.get("clientid")
            secretkey = request.POST.get("secretkey")
            secret_key = secretkey
            redirect_uri = "https://smart-algo.in/fyerslogin"
            response_type = "code"
            state = "success"

            session=accessToken.SessionModel(
                client_id=client_id,
                secret_key=secret_key,
                redirect_uri=redirect_uri,
                response_type=response_type,
                grant_type="authorization_code",
                state=state
            )

            response = session.generate_authcode()
            request.session['client_id']=client_id
            request.session['secret_key']=secret_key
            request.session['redirect_uri']=redirect_uri
            request.session['response_type']=response_type

            apiob = fyersapi(apiuser=userr,apiname=name,clientid=client_id,secretkey=secretkey)
            apiob.save()
            return redirect(response)
        except Exception as e:
            messages.error(request,f"Invalid Credentials")
            return redirect('/createfyersapi')
    else:
        return render(request,"createfyersapi.html")

def fyerslogin(request):
    if request.GET.get('s') == "ok":
        try:
            apiob = fyersapi.objects.filter(apiuser=request.user).first()
            auth_code = request.GET.get("auth_code")
            client_id = request.session['client_id']
            secret_key = request.session['secret_key']
            redirect_uri = request.session['redirect_uri']
            response_type = request.session['response_type']
            session=accessToken.SessionModel(
                client_id=client_id,
                secret_key=secret_key,
                redirect_uri=redirect_uri,
                response_type=response_type,
                grant_type="authorization_code",
            )
            session.set_token(auth_code)
            response = session.generate_token()
            accesstoken = response["access_token"]
            saveapi = fyersapi(apiid=apiob.apiid,apiuser=apiob.apiuser,apiname=apiob.apiname,clientid=apiob.clientid,secretkey=apiob.secretkey,authcode=auth_code,accesstoken=accesstoken)
            saveapi.save()
            messages.success(request,"FYERS Api Created Successfully.")
        except Exception as e:
            try:
                delete=fyersapi(apiid=apiob.apiid)
                delete.delete()
                messages.success(request,"Failed to Authenticate. Plese try after sometime.")
            except:
                messages.success(request,"Failed to Authenticate. Plese try after sometime.")
        return redirect("/dashboard")
    else:
        return redirect("/dashboard")

@login_required
def modifyfyersapi(request,apiid):
    current_api = fyersapi.objects.filter(apiid=apiid).first()
    if current_api.apiuser != request.user:
        return redirect('/')
    if request.method == "POST":
        userr = request.user
        name = request.POST.get("name")
        clientid = request.POST.get("clientid")
        secretkey = request.POST.get("secretkey")
        apiob = fyersapi(apiid=current_api.apiid,apiuser=userr,apiname=name,clientid=clientid,secretkey=secretkey,authcode=current_api.authcode,accesstoken=current_api.accesstoken,datetime=datetime.now())
        apiob.save()
        messages.success(request,"Changes applied Successfully.")
        return redirect("/dashboard")
    else:
        return render(request,'modifyfyers.html',{"current_api":current_api})

@login_required
def deletefyersapi(request,apiid):
    current_api = fyersapi.objects.filter(apiid = apiid).first()
    if current_api.apiuser != request.user:
        return redirect('/')
    delete=fyersapi(apiid=apiid)
    delete.delete()
    messages.success(request,"API deleted successfully")
    return redirect("/dashboard")


# WEBHOOK ALERT
@csrf_exempt
def alert(request,url):
    if request.method == 'POST':
        ob = webhookurl.objects.filter(url = url)
        if ob.__len__() == 0:
            return redirect("/login")
        else:
            ob = ob.first()
            if ob.use == 'webhook':
                if datetime.now().time() > ob.close_time or datetime.now().time() < ob.open_time:
                    return redirect("/")
            elif ob.use == 'time_slot':
                if datetime.now().minute >= ob.slot:
                    return redirect("/")
        status= ""
        json_data = json.loads(request.body)
        syntaxcount = json_data["syntaxcount"]
        # broker = json_data[0]["broker"]
        count = 1
        err = ""
        in_token = IndexTokens.objects.first()
        BANKNIFTY = in_token.BANKNIFTY
        CRUDEOIL = in_token.CRUDEOIL
        SENSEX = in_token.SENSEX
        NIFTY = in_token.NIFTY
        FININFTY = in_token.FIN_NIFTY
        BANKEX = in_token.BANKEX

        err = err + SENSEX
        while(count <= syntaxcount):
            syntax = "syntax"+str(count)
            broker = json_data[syntax]["broker"]
            if json_data[syntax]['option'] == 'True':
                index_list = {'BANKNIFTY':{'segment': 'NSE', 'symbol': 'BANKNIFTY', 'token': BANKNIFTY},'CRUDEOIL':{'segment': 'MCX', 'symbol': 'CRUDEOIL', 'token': CRUDEOIL},'SENSEX':{'segment': 'BSE', 'symbol': 'SENSEX', 'token': SENSEX},'NIFTY':{'segment': 'NSE', 'symbol': 'NIFTY', 'token': NIFTY},'BANKEX':{'segment': 'BSE', 'symbol': 'BANKEX', 'token': BANKEX},'FINNIFTY':{'segment': 'NSE', 'symbol': 'FINNIFTY', 'token': FININFTY}}
                src_symbollist = json.loads(search_symbollist)
                try:
                    from trade.alerts.webhook import get_price
                    syb = get_symbol(json_data[syntax]['symbol'])
                    err = err + "@" + syb
                    detail = index_list.get(syb)
                    token = detail['token']
                    seg = detail['segment']
                    err = err + "@" + seg
                    strike_price = avg_price(int(int(get_price(seg,syb,token))+int(json_data[syntax]['gap'])),int(json_data[syntax]['rate']))
                    err = err + "@ strikeprice " + str(strike_price)
                    newsyb = f"{json_data[syntax]['symbol']}{strike_price}{json_data[syntax]['callput']}"
                    json_data[syntax]['symbol'] = newsyb
                    err = err + "@ newsymbol " + newsyb
                    detail = src_symbollist.get(newsyb)
                    token = detail['token']
                    json_data[syntax]['token'] = token
                except Exception as e:
                    msg = f'Dear Admin, your order placed at  {datetime.datetime.now().time()} failed due to Invalid symbol and token. Error: {e} @ {err}, Syntax Used by you is : {json_data}'
                    notify_admin('Invalid Order for Option', msg)
            if "dhan" in broker:
                f = open("apierr.txt", "a")
                f.write(f'Dhan me aaya \n')
                f.close()
                print('Dhan me aaya')
                dhan_order(syntax,json_data)
            if "angel" in broker:
                angel_order(syntax,json_data)
            if "paisa" in broker:
                paisa_order(syntax,json_data)
            if "alice" in broker:
                alice_order(syntax,json_data)
            if "fyers" in broker:
                fyers_order(syntax,json_data)
            count = count+1
            # Trailing Stoploss
            json_syntax = json_data[syntax]
            for x in json_syntax.keys():
                if x == "trailing_sl":
                    thread = threading.Thread(target=eval_order,args = (json_syntax,))
                    thread.start()
            # Trailing Stoploss END
            # json_data[syntax]['option'] = 'False'
            # ---------END BROKERS-------------
        return HttpResponse(status)
    else:
        return redirect('/')
# ---------END WEBHOOK-------------

# --------------------------API STATUS
@login_required
def status(request):
    if request.method == "POST":
        broker = request.POST.get("broker")
        id = request.POST.get("id")
        apiob = ""
        if broker == "dhan":
            apiob = dhanapi.objects.get(apiid = id)
        elif broker == "paisa":
            apiob = paisaapi.objects.get(apiid = id)
        elif broker == "angel":
            apiob = angelapi.objects.get(apiid = id)
        elif broker == "alice":
            apiob = aliceapi.objects.get(apiid = id)
        elif broker == "fyers":
            apiob = fyersapi.objects.get(apiid = id)
        else:
            return redirect("/dashboard")
        if apiob.is_trading:
                apiob.is_trading = False
                apiob.save()
        else:
            apiob.is_trading = True
            apiob.save()
    return redirect("/dashboard")

# -------------------HISTORY
@login_required
def history(request):
    today = timezone.now().date()
    his = tradebook.objects.filter(apiuser=request.user,datetime__date=today).exclude(broker="").order_by('datetime')
    tpl = 0.0
    plhis = his.filter(status="success")
    dhanob = dhanapi.objects.filter(apiuser=request.user).first()
    angelob = angelapi.objects.filter(apiuser=request.user).first()
    aliceob = aliceapi.objects.filter(apiuser=request.user).first()
    fyersob = fyersapi.objects.filter(apiuser=request.user).first()
    dhan = None
    angel = None
    alice = None
    fyers = None
    if angelob is not None:
        try:
            obj=SmartConnect(api_key=angelob.apikey,
            access_token = angelob.authtoken,
            refresh_token = angelob.rtoken)
            angel = obj.position()
            for x in angel['data']:
                tpl = tpl + x['reliased']
        except:
            pass
    if fyersob is not None:
        try:
            fy = fyersModel.FyersModel(client_id=fyersob.clientid, token=fyersob.accesstoken)
            fyers = fy.positions()
            for x in fyers['netPositions']:
                tpl = tpl + x['realized_profit']
        except:
            pass
    if aliceob is not None:
        try:
            alicebl = Aliceblue(user_id=aliceob.userid,api_key=aliceob.apikey)
            sid = alicebl.get_session_id()
            alice = alicebl.get_daywise_positions()
            for x in alice:
                tpl = tpl + x['realisedprofitloss']
        except:
            pass
    if dhanob is not None:
        dhan = dhanhq(dhanob.clientid,dhanob.accesstoken).get_positions()
        for x in dhan['data']:
            tpl = tpl + x['realizedProfit']
    # for x in plhis:
    #     tpl +=float(x.p_l)
    notification = Notifications.objects.filter(Q(user=request.user) | Q(user=al))
    not_seen = Notifications.objects.filter(Q(user=request.user) | Q(user=al)).filter(seen=False).__len__()
    context = {
        "dhan":dhan,
        "alice":alice,
        "angel":angel,
        "fyers":fyers,
        "his":his,
        "tpl":tpl,
        "notification":notification,
        "not_seen":not_seen
               }
    return render(request,'history.html',context)




@login_required
def save_history(request):
    dhanob = dhanapi.objects.filter(apiuser=request.user).first()
    angelob = angelapi.objects.filter(apiuser=request.user).first()
    aliceob = aliceapi.objects.filter(apiuser=request.user).first()
    fyersob = fyersapi.objects.filter(apiuser=request.user).first()
    for angelob in angelapi.objects.all():
        if angelob is not None:
            try:
                obj=SmartConnect(api_key=angelob.apikey,
                access_token = angelob.authtoken,
                refresh_token = angelob.rtoken)
                angel = obj.position()
                for x in angel['data']:
                    if int(x['totalbuyavgprice']) == 0 or int(x['totalsellavgprice']) == 0:
                        pass
                    else:
                        tradeHistory.objects.create(user=angelob.apiuser,client_id=angelob.clientid,symbol=x['tradingsymbol'],quantity=x['buyqty'],buy_avg=x['totalbuyavgprice'],sell_avg=x['totalsellavgprice'],pnl=x['realised'])
            except:
                pass
    for fyersob in fyersapi.objects.all():
        if fyersob is not None:
            try:
                fy = fyersModel.FyersModel(client_id=fyersob.clientid, token=fyersob.accesstoken)
                fyers = fy.positions()
                for x in fyers['netPositions']:
                    if int(x['buyAvg']) == 0 or int(x['sellAvg']) == 0:
                        pass
                    else:
                        tradeHistory.objects.create(user=fyersob.apiuser,client_id=fyersob.clientid,symbol=x['symbol'],quantity=x['buyQty'],buy_avg=x['buyAvg'],sell_avg=x['sellAvg'],pnl=x['realized_profit'])
            except:
                pass
    for aliceob in aliceapi.objects.all():
        if aliceob is not None:
            try:
                alicebl = Aliceblue(user_id=aliceob.userid,api_key=aliceob.apikey)
                sid = alicebl.get_session_id()
                alice = alicebl.get_daywise_positions()
                for x in alice:
                    if int(x['Buyavgprc']) == 0 or int(x['Sellavgprc']) == 0:
                        pass
                    else:
                        tradeHistory.objects.create(user=aliceob.apiuser,client_id=aliceob.clientid,symbol=x['Tsym'],quantity=x['Bqty'],buy_avg=x['Buyavgprc'],sell_avg=x['Sellavgprc'],pnl=x['realisedprofitloss'])
            except:
                pass
    for dhanob in dhanapi.objects.all():
        if dhanob is not None:
            dhan = dhanhq(dhanob.clientid,dhanob.accesstoken).get_positions()
            for x in dhan['data']:
                if int(x['buyAvg']) == 0 or int(x['sellAvg']) == 0:
                    pass
                else:
                    tradeHistory.objects.create(user=dhanob.apiuser,client_id=dhanob.clientid,symbol=x['tradingSymbol'],quantity=x['buyQty'],buy_avg=x['buyAvg'],sell_avg=x['sellAvg'],pnl=x['realizedProfit'])
    return redirect('/admin/')







def tradestatus(request):
    today = timezone.now().date()
    his = tradebook.objects.filter(apiuser=request.user,datetime__date=today)
    notification = Notifications.objects.filter(Q(user=request.user) | Q(user=al))
    not_seen = Notifications.objects.filter(Q(user=request.user) | Q(user=al)).filter(seen=False).__len__()
    return render(request,'status.html',{"his":his,"notification":notification,"not_seen":not_seen})

# ----------CONTACT US
@login_required
def help(request):
    if request.method == "POST":
        userr=request.user
        numemail = request.POST.get("numemail")
        issue = request.POST.get("issue")
        contactob = contactform(user=userr,numemail=numemail,issue=issue)
        contactob.save()
        messages.success(request,"We will contact to you shortly")
        return redirect("/dashboard")
    else:
        notification = Notifications.objects.filter(Q(user=request.user) | Q(user=al))
        not_seen = Notifications.objects.filter(Q(user=request.user) | Q(user=al)).filter(seen=False).__len__()
        return render(request,'contact.html',{"notification":notification,"not_seen":not_seen})




@login_required
def ststatus(request):
    if request.method == "POST":
        id = request.POST.get("id")
        ob = allstratergy.objects.get(id=id)
        if ob.is_trading:
                ob.is_trading = False
                ob.save()
        else:
            ob.is_trading = True
            ob.save()
    return redirect("/dashboard")


# POLICY
def privacypolicy(request):
    return render(request,"privacypolicy.html")

def refundpolicy(request):
    return render(request,"refundpolicy.html")

def about(request):
    return render(request,"about.html")

def terms(request):
    return render(request,"terms.html")

def pricing(request):
    basic = plans.objects.filter(plan_type='Basic').first()
    pro = plans.objects.filter(plan_type='Pro').first()
    vip = plans.objects.filter(plan_type='VIP').first()
    premium = plans.objects.filter(plan_type='Premium').first()
    context = {
        'basic':basic,
        'pro':pro,
        'vip':vip,
        'premium':premium,
    }
    return render(request,"pricing.html",context=context)


# PLAN
@login_required
def plan(request):
    if request.method == "POST":
        try:
            now = timezone.now()
            expiry_date = now
            p = request.POST.get("plan")
            plan_type = ""
            pay = 0
            if p == "free":
                pay = 0
                plan_type = "Free"
                expiry_date = now + timedelta(days=7)
                person = allplan.objects.filter(user=request.user,plan_type=plan_type).first()
                if allplan.objects.filter(user=request.user,active = True).exists():
                    messages.error(request,'Already Suscribed to a Plan !')
                    return redirect('/profile')
                elif allplan.objects.filter(user=request.user,plan_type=plan_type).exists():
                    messages.error(request,'OOps ! Your have already suscribed to a Free plan')
                    return redirect('/plan')
                else:
                    allplan.objects.create(user=request.user,expiry_date=expiry_date,plan_type=plan_type,order_id='FREE_PLAN_000',active=True,totalorder_perday=10)
                    messages.success(request,'Congratulations ! You unlocked a Free Plan.')
                    return redirect('/profile')
            elif p == "basic":
                plan_type = "Basic"
                pay = plans.objects.filter(plan_type=plan_type).first().after_discount_price
                expiry_date = now + timedelta(days=30)
            elif p == "pro":
                plan_type = "Pro"
                pay = plans.objects.filter(plan_type=plan_type).first().after_discount_price
                expiry_date = now + timedelta(days=30)
            elif p == "vip":
                plan_type = "VIP"
                pay = plans.objects.filter(plan_type=plan_type).first().after_discount_price
                expiry_date = now + timedelta(days=30)
            elif p == "premium":
                plan_type = "Premium"
                pay = plans.objects.filter(plan_type=plan_type).first().after_discount_price
                expiry_date = now + timedelta(days=30)
            else:
                messages.error(request,"Plese select a valid plan !")
                return redirect("/plan")
            person = allplan.objects.filter(user=request.user,plan_type=plan_type).first()
            if allplan.objects.filter(user=request.user,plan_type=plan_type).exists():
                order_id = person.order_id
            else:
                order_id = orderid()
                person = allplan.objects.create(
                    user=request.user,
                    expiry_date=expiry_date,
                    plan_type=plan_type,
                    order_id=order_id,
                    active=False
                )
                person.save()
            url = "https://apiqr.upibuz.in/order/paytm"
            data = {
                "upiuid": "paytmqr28100505010110sggy9gsszk@paytm",
                "token": "82e16b-54fd81-687682-f76ade-14d412",
                "orderId": order_id,
                "txnAmount": str(pay),
                "txnNote": "smartalgo",
                "callback_url": f"https://smart-algo.in/payment_success/{order_id}",
                "cust_Mobile":"0000000000",
                "cust_Email":"smart-algo@gmail.com",
            }
            original_key = '4xGhRSabz1'
            original_key_bytes = original_key.encode('utf-8')
            key = (original_key_bytes + b'\0' * (16 - len(original_key_bytes)))[:16].decode()
            checksum = RechPayChecksum.generateSignature(data,key)
            person.checksum = checksum
            person.save()
            data["checksum"] = checksum
            return render(request,"pay.html",{"data":data})
        except Exception as e:
            messages.warning(request,"Invalid request. Please try after some time.")
            return redirect("/dashboard")
    else:
        notification = Notifications.objects.filter(Q(user=request.user) | Q(user=al))
        not_seen = Notifications.objects.filter(Q(user=request.user) | Q(user=al)).filter(seen=False).__len__()
        basic = plans.objects.filter(plan_type='Basic').first()
        pro = plans.objects.filter(plan_type='Pro').first()
        vip = plans.objects.filter(plan_type='VIP').first()
        premium = plans.objects.filter(plan_type='Premium').first()
        eve = Events.objects.all().first()
        return render(request,"plan.html",{"notification":notification,"not_seen":not_seen,"basic":basic,"pro":pro,"vip":vip,"premium":premium,"eve":eve})


@csrf_exempt
def payment_success(request,order_id):
    try:
        person = allplan.objects.filter(order_id=order_id).first()
        if request.POST.get("status") == 'SUCCESS':
            person.active = True
            person.save()
            messages.success(request,"Congratulations ! Plan has been successfully suscribed.")
            return redirect("/profile")
        else:
            messages.error(request,"Payment Cancelled. Please contact us for further details.")
            return redirect("/plan")
    except:
        messages.error(request,"Payment Cancelled. Invalid request")
        return redirect("/dashboard")


# STRATERGY
@login_required
def strat(request):
    if request.method == "POST":
        try:
            #  Suscription Check
            try:
                ex = allplan.objects.filter(user=request.user).filter(active=True).first()
                today = timezone.now().date()
                if ex.expiry_date.date() == today:
                    ex.delete()
                    messages.warning(request,"Your Plan has been expired today. Upgrade Now")
            except:
                pass
            stratob = allstratergy.objects.filter(user=request.user)
            tlen = stratob.__len__()
            person = allplan.objects.filter(user=request.user).filter(active=True).first()
            try:
                if person.plan_type == "Basic":
                    if tlen >= 2:
                        messages.error(request,"Max API limit reached. Please Upgrade your plan to add more.")
                        return redirect("/dashboard")
                elif person.plan_type == "Pro":
                    if tlen >= 4:
                        messages.error(request,"Max API limit reached. Please Upgrade your plan to add more.")
                        return redirect("/dashboard")
                elif person.plan_type == "VIP":
                    if tlen >= 6:
                        messages.error(request,"Max API limit reached. Please Upgrade your plan to add more.")
                        return redirect("/dashboard")
                elif person.plan_type == "Premium":
                    if tlen >= 10:
                        messages.error(request,"Max API limit reached. Please Upgrade your plan to add more.")
                        return redirect("/dashboard")
                else:
                    messages.error(request,"Please suscribe to a plan to continue.")
                    return redirect("/plan")
            except:
                messages.error(request,"Please suscribe to a plan to continue.")
                return redirect("/plan")
            # Suscription Check Complete
            userr=request.user
            stra = request.POST.get("strategy")
            seg = request.POST.get("segment")
            sym = request.POST.get("symbol")
            quantity = request.POST.get("quantity")
            ptype = request.POST.get("producttype")
            otype = request.POST.get("ordertype")
            broker = request.POST.get("broker")
            ind = broker.find(":")
            brokerapi = broker[0:ind]
            brokerapiid = broker[ind+1:]
            stra=strategy.objects.filter(stg=stra).first()
            seg=segment.objects.filter(segment_name=seg).first()
            ptype=producttype.objects.filter(type=ptype).first()
            otype=ordertype.objects.filter(type=otype).first()
            ob = allstratergy(user=userr,symbol=sym,quantity=quantity,segment=seg,strategy=stra,order_type=otype,product_type=ptype,broker=brokerapi,apiid=brokerapiid)
            ob.save()
            messages.success(request,"Strategy Added Successfully")
        except Exception as e:
            messages.error(request,f"Failed to create strategy {e}")
        return redirect("/dashboard")
    else:
        return redirect("/dashboard")

def modifystratergy(request,id):
    if request.method == "POST":
        userr=request.user
        sym = request.POST.get("symbol")
        quantity = request.POST.get("quantity")
        seg = request.POST.get("segment")
        str = request.POST.get("strategy")
        otype = request.POST.get("ordertype")
        ptype = request.POST.get("producttype")
        broker = request.POST.get("broker")
        price = request.POST.get("price")
        brackcount = request.POST.get("brackcount")
        syntax = request.POST.get("syntax")
        ob = allstratergy(id=id,user=userr,symbol=sym,quantity=quantity,segment=seg,strategy=str,ordertype=otype,producttype=ptype,broker=broker,brackcount=brackcount,syntax=syntax,price=price)
        ob.save()
        messages.success(request,"Strategy Modified Successfully")
        return redirect("/dashboard")
    else:
        s = allstratergy.objects.get(id = id)
        sym = symbol.objects.all()
        seg = segment.objects.all()
        str = strategy.objects.all()
        otype = ordertype.objects.all()
        ptype = producttype.objects.all()
        return render(request,'modifystratergy.html',{"sym":sym,"seg":seg,"str":str,"otype":otype,"ptype":ptype,"s":s})

@login_required
def deletestratergy(request,id):
    delete=allstratergy(id=id)
    delete.delete()
    messages.error(request,"Stratergy deleted successfully")
    return redirect("/dashboard")

# ADMIN STRATERGY
@login_required
@permission_required('is_superuser')
@user_passes_test(lambda u: u.is_superuser)
def targetorder(request):
    ob=allstratergy.objects.all()
    ptype = producttype.objects.all()
    otype = ordertype.objects.all()
    seg = segment.objects.all()
    context = {
        "ob":ob,
        "ptype":ptype,
        "otype":otype,
        "seg":seg,
    }
    if request.method == "POST":
        order = ""
        status= ""
        hquantity="0"
        hsymbol="s"
        hbuy = 0
        hsell= 0
        status = ""
        getsegment = request.POST.get("segment")
        getsymbol = request.POST.get("symbol")
        getprice = request.POST.get("price")
        getstoploss = request.POST.get("stoploss")
        getsquareoff = request.POST.get("squareoff")
        gettrailingstoploss = request.POST.get("trailingstoploss")
        getvariety = request.POST.get("variety")
        getproducttype = request.POST.get("producttype")
        getordertype = request.POST.get("ordertype")
        gettransactiontype = request.POST.get("transactiontype")
        gettoken = symbol.objects.filter(symbol_name=getsymbol).first()
        getsymboltoken = gettoken.symbol_id
        stratob=allstratergy.objects.filter(symbol=gettoken)
        # --------------------------ANGEL ONE --------------------------------------------
        for x in stratob:
            if x.broker == "Angel ONE":
                apiob = angelapi.objects.filter(apiid=x.apiid).first()
                try:
                    clientid = apiob.clientid
                    rtoken = apiob.rtoken
                    apikey = apiob.apikey
                    authtoken = apiob.authtoken
                    obj=SmartConnect(api_key=apikey,
                            access_token = authtoken,
                            refresh_token = rtoken)
                    data =  {
                        "variety": getvariety,
                        "tradingsymbol": getsymbol,
                        "symboltoken": getsymboltoken,
                        "transactiontype": gettransactiontype,
                        "exchange": getsegment,
                        "ordertype": getordertype,
                        "producttype": getproducttype,
                        "duration": "DAY",
                        "price": getprice,
                        "squareoff": getsquareoff,
                        "stoploss": getstoploss,
                        "quantity": x.quantity,
                        "trailingStopLoss":int(gettrailingstoploss)
                    }
                    orderid=obj.placeOrder(data)
                    book = obj.orderBook()["data"]
                    for i in book:
                        if i["orderid"] == orderid:
                            order = str(i)
                            hbuy = str(i["averageprice"])
                            hsell= str(i["averageprice"])
                            if str(i["status"]) == "rejected":
                                status="rejected"
                            else:
                                status="success"
                    hquantity = x.quantity
                    hsymbol = getsymbol.upper()
                    if gettransactiontype.upper() == "BUY":
                        hbuy=float(hbuy)
                        trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                        trade.save()
                    elif gettransactiontype.upper() == "SELL":
                        today = timezone.now().date()
                        old = tradebook.objects.filter(apiuser=x.user,datetime__date=today,symbol=hsymbol).order_by('datetime').reverse().first()
                        old.response = (order)
                        old.sell=float(hsell)
                        old.p_l = (float(old.sell)*float(x.quantity))-(float(old.buy)*float(x.quantity))
                        old.save()
                    status="success"
                    messages.success(request,f"Order Placed successfully.")
                except Exception as e:
                    status="failed"
                    messages.error(request,f"Order Failed due to {e}")
                x.status = status
                x.save()
            # ---------------------Dhan HQ-------------------
            elif x.broker == "Dhan HQ":
                try:
                    apiob = dhanapi.objects.filter(apiid=x.apiid).first()
                    clientid = apiob.clientid
                    accesstoken = apiob.accesstoken
                    dhan = dhanhq(clientid,accesstoken)
                    transactiontype = f"dhan.{gettransactiontype.upper()}"
                    transactiontype = eval(transactiontype)
                    segm = f"dhan.{getsegment.upper()}"
                    segm = eval(segm)
                    protype = f"dhan.{getproducttype.upper()}"
                    protype = eval(protype)
                    ordtype = f"dhan.{getordertype.upper()}"
                    ordtype = eval(ordtype)
                    order = dhan.place_order(
                        tag='smart-algo',
                        transaction_type=transactiontype,
                        exchange_segment=segm,
                        product_type=protype,
                        order_type=ordtype,
                        validity='DAY',
                        security_id=int(getsymboltoken),
                        quantity=int(x.quantity),
                        disclosed_quantity=0,
                        price=int(getprice),
                        after_market_order=False,
                        amo_time='OPEN',
                        bo_profit_value=0,
                        bo_stop_loss_Value=float(getstoploss),
                        drv_expiry_date=None,
                        drv_options_type=None,
                        drv_strike_price=None
                    )
                    try:
                        status = order["status"].lower()
                        order_id = order["data"]["orderId"]
                        book = dhan.get_trade_book(order_id)
                        hquantity = book["data"][0]["tradedQuantity"]
                        hsymbol = book["data"][0]["tradingSymbol"]
                        if gettransactiontype.upper() == "BUY":
                            hbuy = book["data"][0]["tradedPrice"]
                        else:
                            hsell = book["data"][0]["tradedPrice"]
                        order = book
                    except Exception as e:
                        messages.error(request,f"Order Failed due to {e}")
                        status = "failed"
                    hquantity = x.quantity
                    hsymbol = getsymbol.upper()
                    if gettransactiontype.upper() == "BUY":
                        hbuy=float(hbuy)
                        trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                        trade.save()
                    elif gettransactiontype.upper() == "SELL":
                        today = timezone.now().date()
                        old = tradebook.objects.filter(apiuser=x.user,datetime__date=today,symbol=hsymbol).order_by('datetime').reverse().first()
                        old.response = order
                        old.sell=float(hsell)
                        old.p_l = (float(old.sell)*float(x.quantity))-(float(old.buy)*float(x.quantity))
                        old.save()
                    else:
                        pass
                except Exception as e:
                    messages.error(request,f"Order Failed due to {e}")
                    status="failed"
                x.status = status
                x.save()
                    # --------------Alice Blue -----------------
            elif x.broker == "Alice Blue":
                try:
                    apiob = aliceapi.objects.filter(apiid=x.apiid).first()
                    clientid = apiob.userid
                    apitoken = apiob.apikey
                    alice = Aliceblue(user_id=clientid,api_key=apitoken)
                    alice.get_session_id()
                    transactiontype = f"TransactionType.{gettransactiontype}"
                    transactiontype = eval(transactiontype)
                    ordtype = f"OrderType.{getordertype}"
                    ordtype = eval(ordtype)
                    protype = f"ProductType.{getproducttype}"
                    protype = eval(protype)
                    exchange = getsegment
                    sym = getsymbol
                    order = alice.place_order(transaction_type = transactiontype,
                        instrument = alice.get_instrument_by_symbol(exchange, sym),
                        quantity = int(x.quantity),
                        order_type = ordtype,
                        product_type = protype,
                        price = float(getprice),
                        stop_loss = eval(getstoploss),
                        square_off = eval(str(getsquareoff)),
                        trailing_sl = eval(str(gettrailingstoploss)),
                        is_amo = False,
                        order_tag='smart-algo')
                    status="success"
                    o = order["NOrdNo"]
                    ord = alice.get_order_history(o)
                    order = alice.get_order_history(ord["Nstordno"])
                    if gettransactiontype.upper() == "BUY":
                        hbuy = order["Avgprc"]
                    else:
                        hsell = order["Avgprc"]
                    hsymbol = order["Trsym"]
                    hsymbol = getsymbol
                    hquantity = x.quantity
                    if gettransactiontype.upper() == "BUY":
                        hbuy=float(hbuy)
                        trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                        trade.save()
                    elif transactiontype.upper() == "SELL":
                        today = timezone.now().date()
                        old = tradebook.objects.filter(apiuser=x.user,datetime__date=today,symbol=hsymbol).order_by('datetime').reverse().first()
                        old.response = order
                        old.sell=float(hsell)
                        old.p_l = (float(old.sell)*float(x.quantity))-(float(old.buy)*float(x.quantity))
                        old.save()
                    else:
                        pass
                except Exception as e:
                    messages.error(request,f"Order Failed due to {e}")
                    status="failed"
                    order = e
                    trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy,sell=hsell)
                    trade.save()
                x.status = status
                x.save()
            elif x.broker == "5 Paisa":
                OrderType = ""
                Exchange = ""
                ExchangeType = ""
                # ORDER TYPE
                if gettransactiontype.upper() == "BUY":
                    OrderType = "B"
                else:
                    OrderType = "S"
                # EXCHANGE
                if getsegment.upper() == "NSE":
                    Exchange = "N"
                elif getsegment.upper() == "BSE":
                    Exchange = "B"
                else:
                    Exchange = "M"
                # EXCHANGE TYPE
                if getproducttype.upper() == "CASH":
                    ExchangeType = "C"
                elif getproducttype.upper() == "DERIVATIVE":
                    ExchangeType = "D"
                else:
                    ExchangeType = "U"
                try:
                    apiob = paisaapi.objects.filter(apiid=x.apiid).first()
                    cred={
                        "APP_NAME":apiob.apiname,
                        "APP_SOURCE":apiob.appsource,
                        "USER_ID":apiob.userid,
                        "PASSWORD":apiob.password,
                        "USER_KEY":apiob.userkey,
                        "ENCRYPTION_KEY":apiob.encryptionkey
                    }
                    client = FivePaisaClient(cred=cred)
                    totp = pyotp.TOTP(apiob.secretkey, interval=30)
                    tcode = totp.now()
                    client.get_totp_session(apiob.clientcode,tcode,apiob.mpin)
                    o = client.place_order(OrderType=OrderType,Exchange=Exchange,ExchangeType=ExchangeType,ScripCode = int(getsymboltoken), Qty=x.quantity, Price=int(getprice),StopLossPrice=int(getstoploss))
                    messages.error(request,o)
                    status="success"
                    book = client.order_book()
                    for i in book:
                        if i["BrokerOrderId"] == o["BrokerOrderID"]:
                            order = client.get_trade_history(i["ExchOrderID"])
                    hquantity = x.quantity
                    if OrderType.upper() == "B":
                        hbuy = order["TradeHistoryData"][0]["TradePrice"]
                    else:
                        hsell = order["TradeHistoryData"][0]["TradePrice"]
                    if order == None:
                        order = "Invalid Credentials"
                        status="Failed"
                    hsymbol = order["TradeHistoryData"][0]["Symbol"]
                    hquantity = x.quantity
                    if OrderType.upper() == "B":
                        hbuy=float(hbuy)
                        trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker="5 Paisa",status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                        trade.save()
                    elif OrderType.upper() == "S":
                        today = timezone.now().date()
                        old = tradebook.objects.filter(apiuser=x.user,datetime__date=today,symbol=hsymbol).order_by('datetime').reverse().first()
                        old.response = order
                        old.sell=float(hsell)
                        old.p_l = (float(old.sell)*float(x.quantity)-(float(old.buy)*float(x.quantity)))
                        old.save()
                    else:
                        pass
                except Exception as e:
                    messages.error(request,f"Order Failed due to {e}")
                    status="failed"
                    order = e
                    trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker="5 PAISA",status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy,sell=hsell)
                    trade.save()
                x.status = status
                x.save()
                # END 5 PAISA
            elif x.broker == "Fyers":
                try:
                    apiob = fyersapi.objects.filter(apiid=x.apiid).first()
                    clientid = apiob.clientid
                    accesstoken = apiob.accesstoken
                    fyers = fyersModel.FyersModel(client_id=clientid, token=accesstoken)
                    fsymbol=f"{getsegment.upper()}:{getsymbol}"
                    side = 1
                    if gettransactiontype.upper() == "BUY":
                        side=1
                    else:
                        side=-1
                    data = {
                        "symbol":fsymbol,
                        "qty":x.quantity,
                        "type":'L',
                        "side":side,
                        "productType":"BO",
                        "limitPrice":int(getprice),
                        "stopPrice":int(getstoploss),
                        "validity":"DAY",
                        "takeProfit":int(getstoploss)
                    }
                    order = fyers.place_order(data)
                    status= "success"
                    hquantity = x.quantity
                    hsymbol = getsymbol.uppper()
                    if side == 1:
                        hbuy = getprice
                    else:
                        hsell = getprice
                    hsymbol = getsymbol
                    hquantity = x.quantity
                    if side == 1:
                        hbuy=float(hbuy)
                        trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy)
                        trade.save()
                    elif side == -1:
                        today = timezone.now().date()
                        old = tradebook.objects.filter(apiuser=x.apiuser,datetime__date=today,symbol=hsymbol).reverse().first()
                        old.response = order
                        old.sell=float(hsell)
                        old.p_l = (float(old.sell)*float(x.quantity))-(float(old.buy)*float(x.quantity))
                        old.save()
                    else:
                        pass
                except Exception as e:
                    status="failed"
                    messages.error(request,f"Order Failed due to {e}")
                trade = tradebook(apiid=x.apiid,response=order,apiuser=x.user,broker=x.broker,status=status,quantity=hquantity,symbol=hsymbol,buy=hbuy,sell=hsell)
                trade.save()
                x.status = status
                x.save()
            else:
                messages.error(request,"Invalid Api Selected.")
        return redirect('/admin/')
    else:
        return redirect('/admin/')


@login_required
@permission_required('is_superuser')
@user_passes_test(lambda u: u.is_superuser)
def resetorder(request):
    if request.method == "POST":
        ob = allplan.objects.all().update(placed_order = 0)
        messages.success(request,'All Users orders Reset Successfully.')
    return redirect('/admin/')


# ===========LIMIT ORDER==========
@login_required
@permission_required('is_superuser')
@user_passes_test(lambda u: u.is_superuser)
def limit_order(request):
    if request.method == "POST":
        j_syntax = request.POST.get("j_syntax")
        price = request.POST.get("price")
        count = request.POST.get("count")
        json_data = json.loads(j_syntax)
        thread = threading.Thread(target=palce_limit_order,args=(json_data,price,count))
        thread.start()
        messages.success(request,"Limit order Initiated successfully !")
    return redirect('/admin/')

@login_required
@permission_required('is_superuser')
@user_passes_test(lambda u: u.is_superuser)
def syntax(request):
    return render(request,'admin/syntax.html')


# SYMBOL PAGE
def symbol_search(request):
    top_list = [x for x in symbollist[:15]]
    context={
        "top_list":top_list,
        "symbollist":search_symbollist
    }
    return render(request,"admin/symbol.html",context)


# CUSTOM PAGES
def custom_404(request, exception):
    return redirect('/')

# TEST URLS
from stratergy.models import Executed_Stratergy
def test(request):
    Executed_Stratergy.objects.all().delete()
    return redirect('/')


import datetime
import time
from stratergy.symbols.details import get_price, get_market_data, get_instrument
from threading import Thread

def update_data():
    f = open("once.txt", "a")
    f.write('one \n')
    f.close()
    # # New One Adding
    # start_time = time.time()
    # end_time = start_time + 300
    # temp_list = []
    # strat_syb_dict = {}
    # for x in Alert.objects.filter(function='Activated'):
    #     strat_syb_dict[symbol] = {'low':5000000,'high':0}
    #     temp_list.append(get_instrument(x.token))
    # symbols = ','.join(temp_list)
    # while time.time() < end_time:
    #     from stratergy.models import Alert
    #     try:
    #         market_data = get_market_data(symbols)
    #         for x in market_data:
    #             if int(market_data['data'][x]['last_price']) > strat_syb_dict[x]['high']:
    #                 strat_syb_dict[x]['high'] = int(market_data['data'][x]['last_price'])
    #             if int(market_data['data'][x]['last_price']) < strat_syb_dict[x]['low']:
    #                 strat_syb_dict[x]['low'] = int(market_data['data'][x]['last_price'])
    #     except:
    #         pass
    # # New One Adding
    start_time = time.time()
    end_time = start_time + 21600
    while time.time() < end_time:
        from stratergy.models import Alert
        try:
            from stratergy.models import Stratergy_settings
            ob = Stratergy_settings.objects.all().first()
            if not ob.is_active:
                continue
            temp_list = []
            for x in Alert.objects.filter(function='Activated'):
                temp_list.append(x.symbol)
            symbols = ','.join(temp_list)
            f = open("logging.txt", "a")
            f.write(f'Bot Started at {datetime.datetime.now()} \n')
            f.close()
            market_data = get_market_data(symbols)
            f = open("marketdata.txt", "a")
            f.write(f'{market_data} \n')
            f.close()
            for x in market_data['data']:
                symbol = market_data['data'][x]['instrument_token']
                f = open("symbols.txt", "a")
                f.write(f'{symbol} \n')
                f.close()
                ob = Alert.objects.filter(symbol=symbol).first()
                ob.ltp = int(market_data['data'][x]['last_price'])
                vol = market_data['data'][x]['volume']
                try:
                    vol = int(vol)
                except:
                    vol = 0
                ob.current_volume = vol
                f = open("ltp.txt", "a")
                f.write(f'{ob.ltp} \n')
                f.close()
                ob.save()
            time.sleep(6)
        except Exception as e:
            from stratergy.models import Stratergy_settings
            ob = Stratergy_settings.objects.all().first()
            ob.is_active = False
            ob.save()
            f = open("error.txt", "a")
            f.write(f'Bot Started at {datetime.datetime.now()}, {e} \n')
            f.close()
            time.sleep(5)


@login_required
@permission_required('is_superuser')
@user_passes_test(lambda u: u.is_superuser)
def manualstratergy(request):
    from stratergy.symbols.details import get_market_data
    if get_market_data('NSE_EQ|INE062A01020') is None:
        messages.error(request,'Please recreate Upstox access token !')
    thread = Thread(target=update_data)
    thread.start()
    return redirect('/')


from stratergy.models import Stratergy_settings
def upstox_cred(request):
    if request.method == 'GET':
        try:
            code = request.GET.get('code')
            obj = Stratergy_settings.objects.first()
            obj.code = code
            obj.save()
            data = {
                'code': code,
                'client_id': obj.api_key,
                'client_secret': obj.secret_key,
                'redirect_uri': obj.redirect_uri,
                'grant_type': 'authorization_code',
            }
            url = 'https://api-v2.upstox.com/login/authorization/token'
            response = requests.post(url,data=data)
            response = response.json()
            obj.access_token = response['access_token']
            obj.save()
            return redirect('/admin/stratergy/alert/')
        except Exception as e:
            messages.error(request,'Something went wrong !')
            return redirect('/')



def automatedstratergy(request):
    from stratergy.models import Stratergy_settings
    ob = Stratergy_settings.objects.all().first()
    ob.is_active = True
    ob.save()
    thread = Thread(target=update_data)
    thread.start()
    return redirect('/admin/stratergy/stratergy_settings/')




@login_required
@permission_required('is_superuser')
@user_passes_test(lambda u: u.is_superuser)
def activate_stratergy(request):
    from stratergy.models import Dhan_Settings
    import os
    setting = Dhan_Settings.objects.all().first()
    if setting.is_active:
        setting.is_active = False
        setting.save()
    else:
        setting.is_active = True
        setting.save()
        thread = Thread(target=os.system,args=('python3 manage.py dhan_websocket',))
        thread.start()
        thread2 = Thread(target=os.system,args=('python3 manage.py dhan_websocket2',))
        thread2.start()
        # os.system('python manage.py dhan_websocket')
    return redirect('/admin/stratergy/dhan_settings/')
