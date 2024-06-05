import imaplib
import email
import json
import requests
import datetime

def place_alert(data):
    url = 'https://smart-algo.in/alert/smartorder'
    data = json.loads(data)
    data = json.dumps(data)
    response = requests.post(url,data)
    print('Order Placed')
    print(response.text)


# f = open("alert.txt", "r")
# a = f.read()
# place_alert(a)


# IMAP settings
IMAP_SERVER = 'imap.gmail.com'
EMAIL = 'smrtalgo@gmail.com'
PASSWORD = 'giyx lzxw npey mjoz'

# SMTP settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)


i = 0
import time

start_time = time.time()
end_time = start_time + 320
f = open("logging.txt", "a")
f.write(f'Bot Started at {datetime.datetime.now()} \n')
f.close()
while time.time() < end_time:
    mail.select('inbox')# Select the mailbox you want to search
    # Search for unseen emails with 'tradingview' in the subject
    typ, data = mail.search(None, '(UNSEEN SUBJECT "Alert: tradingview")')
    
    if typ == 'OK':
        print('waiting')
        print(i)
        i = i + 1
        mail_ids = data[0].split()
        for num in mail_ids:
            typ, msg_data = mail.fetch(num, '(RFC822)')
            if typ == 'OK':
                email_message = email.message_from_bytes(msg_data[0][1])
                subject = email_message['Subject']
                print(f"Subject: {subject}")
                print(email_message)
                print("Hello")
                # Get email content
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode("utf-8")
                        print(body)
                        print("Email Content:")
                        f = open("alert.txt", "w")
                        f.write(body)
                        f.close()
                        f = open("alert.txt", "r")
                        a = f.read().replace('\n', '')
                        print(body)
                        place_alert(a)
        
f = open("logging.txt", "a")
f.write(f'Bot Closed at {datetime.datetime.now()} \n')
f.close()

# mail.close()
# mail.logout()
