from .models import *
from trade.alerts.webhook import get_price

def custom_admin_context(request):
    ob=allstratergy.objects.all()
    ptype = producttype.objects.all()
    otype = ordertype.objects.all()
    seg = segment.objects.all()
    price = get_price('NSE','SBIN-EQ','3045')
    context={
        "ob":ob,
        "ptype":ptype,
        "otype":otype,
        "seg":seg,
        "angelob":angelapi.objects.all(),
        "dhanob":dhanapi.objects.all(),
        "aliceob":aliceapi.objects.all(),
        "paisaob":paisaapi.objects.all(),
        "fyersob":fyersapi.objects.all(),
        "price":price,
    }
    return context