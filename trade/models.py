from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime 

User = get_user_model()

status = [
        ('initiated', 'initiated'),
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('failed', 'failed'),
        ('cancelled', 'cancelled'),
    ]

tagchoice = [
        ('webhook', 'webhook'),
        ('smartorder', 'smartorder'),
        ('time_slot', 'time_slot'),
    ]

brokerChoice = [
        ('None', 'None'),
        ('Fyers', 'Fyers'),
        ('Angel ONE', 'Angel ONE'),
        ('Alice Blue', 'Alice Blue'),
        ('Dhan HQ', 'Dhan HQ'),
        ('5 Paisa', '5 Paisa')
    ]

class bot_order_quantity(models.Model):
   user = models.OneToOneField(User,on_delete=models.CASCADE)
   quantity = models.PositiveIntegerField(blank=True, null=True,default=10)
   crudeoil_quantity = models.PositiveIntegerField(blank=True, null=True,default=100)
   nifty_quantity = models.PositiveIntegerField(blank=True, null=True,default=50)
   bank_nifty_quantity = models.PositiveIntegerField(blank=True, null=True,default=15)
   fin_nifty_quantity = models.PositiveIntegerField(blank=True, null=True,default=40)
   bankex_quantity = models.PositiveIntegerField(blank=True, null=True,default=40)
   sensex_quantity = models.PositiveIntegerField(blank=True, null=True,default=10)
   class Meta:
        verbose_name = "Quantity Setting"
        verbose_name_plural = "Quantity Setting"
   def __str__(self):
      return self.user.get_username()

class angelapi(models.Model):
   apiid=models.AutoField(primary_key=True)
   datetime = models.DateTimeField(auto_now_add=True,null=True)
   apiuser=models.ForeignKey(User,on_delete=models.CASCADE)
   apiname = models.CharField(max_length=100,default="xyz")
   clientid = models.CharField(max_length=100,default="xyz")
   password = models.CharField(max_length=100,default="xyz")
   apikey = models.CharField(max_length=100,default="xxxxxxxxxxxx")
   totp = models.CharField(max_length=100,default="1234")
   rtoken = models.CharField(max_length=500,default="refreshtoken")
   authtoken = models.CharField(max_length=2000,default="authtoken")
   is_trading = models.BooleanField(default=False)
   class Meta:
        verbose_name = "Angel API"
        verbose_name_plural = "Angel API"
   def __str__(self):
      return self.apiname

# DHAN
class dhanapi(models.Model):
   apiid=models.AutoField(primary_key=True)
   datetime = models.DateTimeField(auto_now_add=True,null=True)
   apiuser=models.ForeignKey(User,on_delete=models.CASCADE)
   apiname = models.CharField(max_length=100,default="xyz")
   clientid = models.CharField(max_length=100,default="xyz")
   accesstoken = models.CharField(max_length=1000,default="xxxxxxxxxxxx")
   is_trading = models.BooleanField(default=False)
   class Meta:
        verbose_name = "Dhan API"
        verbose_name_plural = "Dhan API"
   def __str__(self):
      return self.apiname

# 5 PAISA
class paisaapi(models.Model):
   apiid=models.AutoField(primary_key=True)
   datetime = models.DateTimeField(auto_now_add=True,null=True)
   apiuser=models.ForeignKey(User,on_delete=models.CASCADE)
   apiname = models.CharField(max_length=100,default="xyz")
   appsource = models.CharField(max_length=100,default="source")
   userid = models.CharField(max_length=100,default="xyz")
   password = models.CharField(max_length=100,default="xyz")
   userkey = models.CharField(max_length=100,default="xxxxxxxxxxxx")
   encryptionkey = models.CharField(max_length=100,default="xxxxxxxxxxxx")
   secretkey = models.CharField(max_length=500,default="secretkey")
   clientcode = models.CharField(max_length=500,default="clientcode")
   mpin = models.CharField(max_length=500,default="123456")
   is_trading = models.BooleanField(default=False)
   class Meta:
        verbose_name = "5Paisa API"
        verbose_name_plural = "5Paisa API"
   def __str__(self):
      return self.apiname

# FYERS
class fyersapi(models.Model):
   apiid = models.AutoField(primary_key=True)
   datetime = models.DateTimeField(auto_now_add=True,null=True)
   apiuser=models.ForeignKey(User,on_delete=models.CASCADE)
   apiname = models.CharField(max_length=100,default="xyz")
   clientid = models.CharField(max_length=100,default="xyz")
   secretkey = models.CharField(max_length=100,default="xxxxxxxxxxxx")
   authcode = models.CharField(max_length=1000,default="xxxxxxxxxxxx")
   accesstoken = models.CharField(max_length=1000,default="xxxxxxxxxxxx")
   is_trading = models.BooleanField(default=False)
   class Meta:
        verbose_name = "Fyers API"
        verbose_name_plural = "Fyers API"
   def __str__(self):
      return self.apiname

# ALICE BLUE   
class aliceapi(models.Model):
   apiid=models.AutoField(primary_key=True)
   datetime = models.DateTimeField(auto_now_add=True,null=True)
   apiuser=models.ForeignKey(User,on_delete=models.CASCADE)
   apiname = models.CharField(max_length=100,default="xyz")
   userid = models.CharField(max_length=100,default="xyz")
   apikey = models.CharField(max_length=500,default="xxxxxxxxxxxx")
   is_trading = models.BooleanField(default=False)
   class Meta:
        verbose_name = "Alice API"
        verbose_name_plural = "Alice API"
   def __str__(self):
      return self.apiname

# HISTORY
class tradebook(models.Model):
   apiid = models.CharField(max_length=500,default="")
   datetime = models.DateTimeField(auto_now_add=True,null=True)
   response = models.CharField(max_length=500,default="")
   status = models.CharField(max_length=500,default="")
   broker = models.CharField(max_length=500,default="")
   apiuser=models.ForeignKey(User,on_delete=models.CASCADE,default="")
   quantity = models.CharField(max_length=500,default="0")
   symbol = models.CharField(max_length=500,default="s")
   buy = models.CharField(max_length=500,default="0")
   p_l = models.FloatField(default=0.0)
   sell = models.CharField(max_length=500,default="0")
   class Meta:
        verbose_name = "Responses"
        verbose_name_plural = "Responses"
   def __str__(self):
      a = "History"
      return a



class tradeHistory(models.Model):
   id=models.AutoField(primary_key=True)
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   broker = models.CharField(max_length=100,default="")
   client_id = models.CharField(max_length=100,default="")
   symbol = models.CharField(max_length=100,default="")
   quantity = models.IntegerField(default=0)
   buy_avg = models.FloatField()
   sell_avg = models.FloatField()
   pnl = models.FloatField()
   date_time = models.DateField(auto_now_add=True,null=True)
   class Meta:
         verbose_name = "Trade History"
         verbose_name_plural = "Trade History"
         unique_together = ('date_time', 'symbol', 'client_id','broker','user')
   def __str__(self):
      return self.symbol




# CONTACT US
class contactform(models.Model):
    contactid = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    numemail=models.CharField(max_length=100,default="")
    issue=models.CharField(max_length=5000,default="")
    datetime = models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
    def __str__(self):
        return self.numemail

   
class segment(models.Model):
   segment_name=models.CharField(max_length=100,default="")
   class Meta:
        verbose_name = "Segment"
        verbose_name_plural = "Segment"
   def __str__(self):
      return self.segment_name
   
class strategy(models.Model):
   stg=models.CharField(max_length=100,default="")
   class Meta:
        verbose_name = "Strategy"
        verbose_name_plural = "Strategy"
   def __str__(self):
      return self.stg

class ordertype(models.Model):
   type=models.CharField(max_length=100,default="")
   def __str__(self):
      return self.type

class producttype(models.Model):
   type=models.CharField(max_length=100,default="")
   def __str__(self):
      return self.type


class allstratergy(models.Model):
   id=models.AutoField(primary_key=True)
   datetime = models.DateTimeField(auto_now_add=True,null=True)
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   quantity=models.CharField(max_length=100,default="0")
   segment=models.ForeignKey(segment,default="",on_delete=models.CASCADE)
   symbol=models.CharField(max_length=100,default="")
   order_type=models.ForeignKey(ordertype,default="",on_delete=models.CASCADE)
   product_type=models.ForeignKey(producttype,default="",on_delete=models.CASCADE)
   broker=models.CharField(max_length=50,choices=brokerChoice,default="None")
   apiid=models.CharField(max_length=100,default="")
   strategy=models.ForeignKey(strategy,default="",on_delete=models.CASCADE)
   status=models.CharField(max_length=100,default="pending")
   class Meta:
        verbose_name = "All Strategy"
        verbose_name_plural = "All Strategy"
   def __str__(self):
      return self.broker

class webhookurl(models.Model):
   id = models.AutoField(primary_key=True)
   datetime = models.DateTimeField(auto_now_add=True,null=True)
   url = models.CharField(max_length=500,default="webhook")
   use=models.CharField(max_length=50,choices=tagchoice,default="webhook")
   slot = models.PositiveIntegerField(blank=True,null=True)
   open_time = models.TimeField(blank=True,null=True)
   close_time = models.TimeField(blank=True,null=True)
   class Meta:
        verbose_name = "Webhook Url"
        verbose_name_plural = "Webhooks"
   def __str__(self):
      a = "https://smart-algo.in/alert/"+self.url
      return a
   


PLAN_CHOICES = [
        ('Free', 'Free'),
        ('Basic', 'Basic -> 1500'),
        ('Pro', 'Pro -> 2500'),
        ('VIP', 'VIP -> 3500'),
        ('Premium', 'Premium -> 4500'),
    ]

class plans(models.Model):
   id=models.AutoField(primary_key=True)
   plan_type = models.CharField(max_length=50,choices=PLAN_CHOICES,default="Expire")
   price = models.PositiveIntegerField(default=0)
   discount = models.PositiveIntegerField(default=0)
   after_discount_price = models.PositiveIntegerField(default=0)
   class Meta:
        verbose_name = "Plan Settings"
        verbose_name_plural = "Plan Settings"
   def __str__(self):
      return self.plan_type
    

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=80, default='')
    content = models.TextField()
    iframe = models.CharField(max_length=200, default='')
    date_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.subject
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"



class allplan(models.Model):
   id=models.AutoField(primary_key=True)
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   suscribed_date = models.DateTimeField(auto_now_add=True,null=True)
   expiry_date = models.DateTimeField()
   plan_type = models.CharField(max_length=50,choices=PLAN_CHOICES,default="Expire")
   order_id = models.CharField(max_length=255,default="")
   checksum = models.CharField(max_length=255,default="")
   active = models.BooleanField(default=False)
   placed_order = models.PositiveIntegerField(default=0,null=True)
   totalorder_perday = models.CharField(max_length=255,default="10")
   class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Subscribers"
   def __str__(self):
      return self.plan_type
   
# NEWS AND BLOG
class news(models.Model):
   id=models.AutoField(primary_key=True)
   date = models.DateTimeField(auto_now_add=True,null=True)
   headline = models.TextField(max_length="1000",default="",null=True)
   class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
   def __str__(self):
      return self.headline
   
class Limitorder(models.Model):
   id=models.AutoField(primary_key=True)
   date = models.DateTimeField(auto_now_add=True,null=True)
   current_price = models.FloatField(default=0.0)
   limit_price = models.FloatField(default=0.0)
   crossed = models.PositiveIntegerField(default=0)
   cross_count = models.PositiveIntegerField(default=0)
   symbol = models.CharField(max_length=200,default="")
   status = models.CharField(choices=status, max_length=12,default="initiated")
   syntax = models.CharField(max_length=1000,default="")
   class Meta:
        verbose_name = "Limit Order"
        verbose_name_plural = "Limit Orders"
   def __str__(self):
      return self.symbol
   
class trailing_stoploss(models.Model):
   id=models.AutoField(primary_key=True)
   date = models.DateTimeField(auto_now_add=True,null=True)
   stoploss = models.FloatField(default=0.0)
   target = models.FloatField(default=0.0)
   ordered_price = models.FloatField(default=0.0)
   exit_avg = models.FloatField(default=0.0)
   current_price = models.FloatField(default=0.0)
   transaction_type = models.CharField(max_length=5,default="BUY")
   symbol = models.CharField(max_length=200,default="")
   status = models.CharField(choices=status, max_length=12,default="initiated")
   message = models.CharField(max_length=100,default="")
   class Meta:
        verbose_name = "Trailing alert"
        verbose_name_plural = "Trailing Alerts"
   def __str__(self):
      return self.symbol
   

class Notifications(models.Model):
   id=models.AutoField(primary_key=True)
   user = models.ManyToManyField(User,blank=True)
   title = models.CharField(max_length=100)
   content = models.TextField()
   date_time = models.DateField(auto_now_add=True)
   seen = models.BooleanField(default=False)
   class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
   def __str__(self):
      return self.title
   
