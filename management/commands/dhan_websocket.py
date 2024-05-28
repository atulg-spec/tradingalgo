from django.core.management.base import BaseCommand
from dhanhq import marketfeed
from django.db.models import Q
from asgiref.sync import sync_to_async
from stratergy.models import StratergyAlert,Dhan_Settings
import os


# Define your DHAN API credentials
setting = Dhan_Settings.objects.all().first()

client_id = setting.client_id
access_token = setting.access_token

# Define the instruments to subscribe to
instruments = [(5, "426247")]

# Define the subscription code
subscription_code = marketfeed.Quote

# Define the callback functions for connection and receiving messages
async def on_connect(instance):
    print("Connected to WebSocket")


async def keep_connection_alive(ws):
    try:
        while True:
            # Wait for Ping from server
            ping_msg = await ws.recv()

            # Respond with Pong to maintain connection
            if ping_msg == b'Ping':
                print('Ping')
                await ws.send('Pong')
    except :
        # Connection closed by server, handle reconnection here
        print("Connection closed by server, reconnecting...")
        # Call your reconnect logic here
        # Example: await connect_to_websocket()


async def on_message(instance, message):
    # instance.subscribe_symbols(1,[(5, "426247"),(1, "3045")])
    instance.subscribe_symbols(1,await get_Tokens())
    token = message['security_id']
    ob = await get_Alert(token)
    # print(message)
    try:
        ob.ltp = int(float(message['LTP']))
        print(ob.ltp)
        ob.current_volume = int(message['volume'])
        await save_alert(ob)
    except Exception as e:
        print(e)



@sync_to_async
def get_Tokens():
    tokenlist = []
    for x in StratergyAlert.objects.all():
        tokenlist.append((x.segment,(x.token)))
    # print(tokenlist)
    return tokenlist
    # return StratergyAlert.objects.filter(token=token).first()


@sync_to_async
def get_Alert(token):
    return StratergyAlert.objects.filter(token=token).first()

@sync_to_async
def save_alert(ob):
    ob.save()

# Create a Django management command class
class Command(BaseCommand):
    help = 'Connect to DHAN API WebSocket and retrieve real-time market data'

    def handle(self, *args, **kwargs):
        print(f"Subscription code: {subscription_code}")

        # Initialize DHAN API WebSocket feed
        if setting.is_active:
            feed = marketfeed.DhanFeed(client_id,
                                   access_token,
                                   instruments,
                                   subscription_code,
                                   on_connect=on_connect,
                                   on_message=on_message)

        # Start the WebSocket feed
            feed.run_forever()
            print('RUN AGAIN')
            os.system('python manage.py dhan_websocket')
