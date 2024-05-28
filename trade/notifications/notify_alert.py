from trade.models import Notifications,get_user_model

User = get_user_model()

def api_notify(user,apiname,broker):
    title = 'Invalid API Credentials'
    content = f'''Dear {user}, Your {apiname} credentials for {broker} have an issue. Verify your details and renew your session. For assistance, contact support at [Support smrtalgo@gmail.com].'''
    ob = Notifications.objects.create(title=title,content=content,seen=False)
    person = User.objects.filter(username=user).first()
    ob.user.add(person)
    ob.save()


def notify_admin(title,message):
    ob = Notifications.objects.create(title=title,content=message,seen=False)
    person = User.objects.filter(username='admin').first()
    ob.user.add(person)
    ob.save()
    