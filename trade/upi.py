
import random
import string
from .models import *
# ORDERID GENERATOR
def orderid(length=10):
    characters = string.ascii_letters + string.digits
    attempts = 0
    while True:
        orderid = ''.join(random.choice(characters) for _ in range(length))
        if not allplan.objects.filter(orderid=orderid).exists():
            return orderid
        attempts += 1

print(orderid())