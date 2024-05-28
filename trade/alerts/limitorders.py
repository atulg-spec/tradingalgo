from trade.models import *
from trade.alerts.webhook import get_price
import json
import requests
import time

def place_order(json_syntax):
    ur = webhookurl.objects.filter(use='smartorder').first()
    url = f'https://smart-algo.in/alert/{ur.url}'
    data = json.dumps(json_syntax)
    response = requests.post(url,data)



def palce_limit_order(json_data,price,count):
    ordered = False
    ttype = json_data['syntax1']['ttype']
    symbol = json_data['syntax1']['symbol']
    token = json_data['syntax1']['token']
    segment = json_data['syntax1']['segment']
    current_price = get_price(segment,symbol,token)
    if current_price == 0.0:
        return False
    order = Limitorder.objects.create(
        limit_price = price,
        current_price = current_price,
        cross_count = int(count),
        symbol = symbol,
        status = 'initiated',
        syntax = json_data
    )
    order.save()
    while not ordered:
        if int(current_price) == int(order.limit_price):
            order.crossed = order.crossed + 1
            order.save()
        if order.status == 'cancelled' or order.status == 'completed':
            ordered = True
        if order.crossed >= order.cross_count:
            place_order(order.syntax)
            order.status = 'completed'
            order.save()
            ordered = True
            break
        time.sleep(1)
        current_price = get_price(segment,symbol,token)
