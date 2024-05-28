from py5paisa import FivePaisaClient
import pyotp

apiname = '5P51014280'
appsource = '17111'
userid = 'VJRSDEgBqLf'
password = 'NKbj46GOIqX'
userkey = '4rxb1w7cpgv2VJVstL42GHT5ss57r4GE'
encryptionkey = 'Mhq0jbrWL5vbzD7QxLfEZtlwnECle5mc'
secretkey = 'GUYTAMJUGI4DAXZVKBDUWRKZ'
clientcode = '51014280'
mpin = '875094'

cred={
    "APP_NAME":apiname,
    "APP_SOURCE":appsource,
    "USER_ID":userid,
    "PASSWORD":password,
    "USER_KEY":userkey,
    "ENCRYPTION_KEY":encryptionkey
}
client = FivePaisaClient(cred=cred)



totp = pyotp.TOTP(secretkey, interval=30)
tcode = totp.now()
order = client.get_totp_session(clientcode,tcode,mpin)
print("--=-=--==-=-=-=-=-=-=-=-=-=-=-")
print("--=-=--==-=-=-=-=-=-=-=-=-=-=-")
o = client.place_order(
    OrderType='B',
    Exchange='N',
    ExchangeType='C',
    ScripCode = 3045,
    Qty=int(1),
    Price=int(0),
    StopLossPrice = int(0),
    IsIntraday=True
    )
status="success"
print(o)
book = client.order_book()
print("=-=-=-=-=-=-=-=-=-=-")
print(book)