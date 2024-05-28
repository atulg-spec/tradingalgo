from django.utils import timezone
from trade.models import *

def get_user_list(condition,syb):
    try:
        users = []
        ob = ""
        if condition.upper() == 'STRATEGY':
            ob = allstratergy.objects.filter(symbol=syb)
            for x in ob:
                users.append(x.user.get_username())
        if 'FREE' in condition.upper():
            ob = allplan.objects.filter(plan_type='Free')
            for x in ob:
                users.append(x.user.get_username())
        if 'BASIC' in condition.upper():
            ob = allplan.objects.filter(plan_type='Basic')
            for x in ob:
                users.append(x.user.get_username())
        if 'PRO' in condition.upper():
            ob = allplan.objects.filter(plan_type='Pro')
            for x in ob:
                users.append(x.user.get_username())
        if 'VIP' in condition.upper():
            ob = allplan.objects.filter(plan_type='VIP')
            for x in ob:
                users.append(x.user.get_username())
        if 'PREMIUM' in condition.upper():
            ob = allplan.objects.filter(plan_type='Premium')
            for x in ob:
                users.append(x.user.get_username())
        print(users)
        return users
    except:
        return False

def present(apiuser,json_syntax):
    symbol = json_syntax['symbol']
    condition = json_syntax['users']
    userlist = get_user_list(condition,symbol)
    if not userlist:
        return False
    print(type(apiuser))
    if str(apiuser) in userlist:
        print("true")
        return True
    else:
        print("false")
        return False

def suscribed(apiuser):
    # Suscription Check
    try:
        try:
            ex = allplan.objects.filter(user=apiuser).filter(active=True).first()
            today = timezone.now().date()
            if ex.expiry_date.date() == today:
                ex.delete()
        except:
            return False
        person = allplan.objects.filter(user=apiuser).filter(active=True).first()
        today = timezone.now().date()
        trbook = tradebook.objects.filter(apiuser=apiuser,datetime__date=today).__len__()
        if int(person.totalorder_perday) <= person.placed_order:
            return False
        return True
    except:
        return False
    # Suscription check completed