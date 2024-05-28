from django.db import models
from trade.models import User
from stratergy.symbols.instruments import get_symbol, get_instrument, get_dhan_symbol
import json
import requests
import datetime
import time

# Create your models here.
stratergy_option = [
        ('Manual Input', 'Manual Input'),
    ]

function_status = [
        ('Activated', 'Activated'),
        ('Deactivated', 'Deactivated'),
    ]

position_status_choices = [
        ('EMPTY', 'EMPTY'),
        ('POSITION_OPEN', 'POSITION_OPEN'),
        ('SCALP_POSITION_OPEN', 'SCALP_POSITION_OPEN'),
        ('POSITION_CLOSED', 'POSITION_CLOSED'),
        ('SCALP_POSITION_CLOSED', 'SCALP_POSITION_CLOSED'),
    ]

class Stratergy_settings(models.Model):
    url = models.CharField(max_length=150,default='https://smart-algo.in/alert/smartorder')
    client_id = models.CharField(max_length=100, default='')
    redirect_uri = models.CharField(max_length=120, default='https://smart-algo.in/upstox_cred')
    api_key = models.CharField(max_length=1000,default='')
    secret_key = models.CharField(max_length=300,default='')
    code = models.CharField(max_length=100, default='Leave it blank')
    access_token = models.CharField(max_length=1000, default='Leave it blank')
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.client_id
    class Meta:
        verbose_name = "Stratergy Setting"
        verbose_name_plural = "Settings"


class Dhan_Settings(models.Model):
    client_id = models.CharField(max_length=100, default='')
    access_token = models.CharField(max_length=1000, default='')
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.client_id
    class Meta:
        verbose_name = "Dhan Setting"
        verbose_name_plural = "Dhan Settings"


class Alert(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True,null=True)
    stratergy = models.CharField(choices=stratergy_option,max_length=50,default="")
    token = models.CharField(max_length=50,default="")
    start_time = models.TimeField()
    end_time = models.TimeField(default='00:00')
    buy_syntax = models.TextField()
    sell_syntax = models.TextField()
    high = models.PositiveIntegerField(default=0)
    low = models.PositiveIntegerField(default=0)
    target = models.PositiveIntegerField(default=0)
    function = models.CharField(choices=function_status,max_length=50,default="")
    # AUTOMATED FIELDS
    symbol = models.CharField(max_length=50,default="-----")
    symbol_name = models.CharField(max_length=50,default="-----")
    ltp = models.PositiveIntegerField(default=0)
    current_volume = models.PositiveIntegerField(default=5000000000000)
    last_volume = models.PositiveIntegerField(default=5000000000000)
    gap = models.IntegerField(default=0)
    position_status = models.CharField(choices=position_status_choices,max_length=50,default="")
    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"
    def save(self, *args, **kwargs):
        self.gap = (self.high - self.low) / 2
        if datetime.datetime.now().time() > self.start_time and datetime.datetime.now().time() < self.end_time:
            if datetime.datetime.now().time().minute == self.start_time.minute:
                self.low = self.ltp
                self.high = self.ltp
            else:
                if self.ltp > self.high:
                    self.high = self.ltp
                if self.ltp < self.low:
                    self.low = self.ltp
            super().save(*args, **kwargs)
        else:
            try:
                if self.position_status == 'EMPTY':
                    if (self.ltp > self.high and self.current_volume >= self.last_volume):
                        try:
                            self.position_status = 'POSITION_OPEN'
                            self.last_volume = self.current_volume
                            self.save()
                            super().save(*args, **kwargs)
                            f = open("order.txt", "a")
                            f.write(f'BUY POSITION {datetime.datetime.now().time()}\n')
                            f.close()
                        # PLACE BUY ORDER
                            Executed_Stratergy.objects.create(symbol=self.symbol_name,remark='Buy Position Created',syntax_used=self.buy_syntax,response="response")
                        except Exception as e:
                            f = open("ordererror.txt", "a")
                            f.write(f'Bot Started at {e} \n')
                            f.close()
                            print(f'Buy error {e}')
                    if (self.ltp < self.low and self.current_volume >= self.last_volume):
                        try:
                            self.position_status = 'SCALP_POSITION_OPEN'
                            self.last_volume = self.current_volume
                            self.save()
                            super().save(*args, **kwargs)
                            # PLACE SELL ORDER
                            f = open("order.txt", "a")
                            f.write(f'SELL POSITION \n')
                            f.close()
                            Executed_Stratergy.objects.create(symbol=self.symbol_name,remark='Sell Position Created',syntax_used=self.sell_syntax,response="response")
                        except Exception as e:
                            f = open("ordererror.txt", "a")
                            f.write(f'Bot Sell at {e} \n')
                            f.close()
                            print(f'Sell error {e}')
                elif self.position_status == 'POSITION_OPEN':
                    if (self.ltp < self.low and self.current_volume >= self.last_volume):
                        try:
                            self.position_status = 'SCALP_POSITION_OPEN'
                            self.last_volume = self.current_volume
                            self.save()
                            super().save(*args, **kwargs)
                            # PLACE SELL ORDER
                            f = open("order.txt", "a")
                            f.write(f'SELL POSITION \n')
                            f.close()
                            Executed_Stratergy.objects.create(symbol=self.symbol_name,remark='Sell Position Created',syntax_used=self.sell_syntax,response="response")
                        except Exception as e:
                            f = open("ordererror.txt", "a")
                            f.write(f'Bot Sell at {e} \n')
                            f.close()
                            print(f'Sell error {e}')
                elif self.position_status == 'SCALP_POSITION_OPEN':
                    if (self.ltp > self.high and self.current_volume >= self.last_volume):
                        try:
                            self.position_status = 'POSITION_OPEN'
                            self.last_volume = self.current_volume
                            self.save()
                            super().save(*args, **kwargs)
                            f = open("order.txt", "a")
                            f.write(f'BUY POSITION {datetime.datetime.now().time()}\n')
                            f.close()
                        # PLACE BUY ORDER
                            Executed_Stratergy.objects.create(symbol=self.symbol_name,remark='Buy Position Created',syntax_used=self.buy_syntax,response="response")
                        except Exception as e:
                            f = open("ordererror.txt", "a")
                            f.write(f'Bot Started at {e} \n')
                            f.close()
                            print(f'Buy error {e}')
            except Exception as e:
                print(f'fullerror {e}')
                f = open("orderwerror.txt", "a")
                f.write(e)
                f.close()
            if (((self.position_status == 'POSITION_CLOSED') and int(self.ltp) <= (int((self.high)-int(self.gap)))) or ((self.position_status == 'SCALP_POSITION_CLOSED') and int(self.ltp) >= (int(self.low)+int(self.gap)))):
                self.position_status = 'EMPTY'
                self.last_volume = self.current_volume
                super().save(*args, **kwargs)
            if (self.ltp >= (int(self.high)+(int(self.target)))):
                self.position_status = 'POSITION_CLOSED'
                self.ltp = self.ltp
                self.last_volume = self.current_volume
                super().save(*args, **kwargs)
            if (self.ltp <= (int(self.low)-(int(self.target)))):
                self.position_status = 'SCALP_POSITION_CLOSED'
                self.ltp = self.ltp
                self.last_volume = self.current_volume
                super().save(*args, **kwargs)
        self.last_volume = self.current_volume
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.id}'



class StratergyAlert(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True,null=True)
    stratergy = models.CharField(choices=stratergy_option,max_length=50,default="")
    segment = models.PositiveIntegerField(default=0)
    token = models.CharField(max_length=50,default="")
    start_time = models.TimeField()
    end_time = models.TimeField()
    buy_syntax = models.TextField()
    sell_syntax = models.TextField()
    high = models.PositiveIntegerField(default=0)
    low = models.PositiveIntegerField(default=5000000000000)
    target = models.PositiveIntegerField(default=0)
    function = models.CharField(choices=function_status,max_length=50,default="")
    # AUTOMATED FIELDS
    symbol = models.CharField(max_length=50,default="-----")
    ltp = models.PositiveIntegerField(default=0)
    bid_Qty = models.PositiveIntegerField(default=0)
    ask_Qty = models.PositiveIntegerField(default=0)
    gap = models.IntegerField(default=0)
    position_status = models.CharField(choices=position_status_choices,max_length=50,default="")
    class Meta:
        verbose_name = "Stratergy Alert"
        verbose_name_plural = "Stratergy Alerts"
    def save(self, *args, **kwargs):
        seg = 'ES'
        if self.segment == 0:
            seg = 'INDEX'
        self.symbol = get_dhan_symbol(self.token,seg)
        self.gap = (self.high - self.low) / 2
        if datetime.datetime.now().time() > self.start_time and datetime.datetime.now().time() < self.end_time:
            if datetime.datetime.now().time().minute == self.start_time.minute:
                self.low = self.ltp
                self.high = self.ltp
            else:
                if self.ltp > self.high:
                    self.high = self.ltp
                if self.ltp < self.low:
                    self.low = self.ltp
            super().save(*args, **kwargs)
        else:
            try:
                if self.position_status == 'EMPTY':
                    if (self.ltp > self.high and self.bid_Qty >= self.ask_Qty):
                        self.position_status = 'POSITION_OPEN'
                        self.save()
                        super().save(*args, **kwargs)
                        f = open("order.txt", "a")
                        f.write(f'BUY POSITION \n')
                        f.close()
                        # PLACE BUY ORDER
                        Executed_Stratergy.objects.create(remark='Buy Position Created',syntax_used=self.buy_syntax,response="response")
                    if (self.ltp < self.low and self.ask_Qty >= self.bid_Qty):
                        self.position_status = 'SCALP_POSITION_OPEN'
                        self.save()
                        super().save(*args, **kwargs)
                        # PLACE SELL ORDER
                        f = open("order.txt", "a")
                        f.write(f'SELL POSITION \n')
                        f.close()
                        Executed_Stratergy.objects.create(remark='Sell Position Created',syntax_used=self.sell_syntax,response="response")
            except:
                pass
            if (((self.position_status == 'POSITION_CLOSED') and int(self.ltp) <= (int((self.high)-int(self.gap)))) or ((self.position_status == 'SCALP_POSITION_CLOSED') and int(self.ltp) >= (int(self.low)+int(self.gap)))):
                self.position_status = 'EMPTY'
                super().save(*args, **kwargs)
            if (self.ltp >= (int(self.high)+(int(self.target)))):
                self.position_status = 'POSITION_CLOSED'
                self.ltp = self.ltp
                super().save(*args, **kwargs)
            if (self.ltp <= (int(self.low)-(int(self.target)))):
                self.position_status = 'SCALP_POSITION_CLOSED'
                self.ltp = self.ltp
                super().save(*args, **kwargs)
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.id}'



from django.utils import timezone
from threading import Thread
class Executed_Stratergy(models.Model):
    id=models.AutoField(primary_key=True)
    datetime = models.DateTimeField(default=timezone.now,null=True)
    symbol = models.CharField(default="",max_length=25)
    remark = models.CharField(max_length=100)
    url = models.CharField(max_length=100,default='https://smart-algo.in/alert/smartorder')
    syntax_used = models.TextField()
    response = models.CharField(max_length=100)
    class Meta:
        verbose_name = "Executed Orders"
        verbose_name_plural = "Order"
    def save(self, *args, **kwargs):
        print('shi baat hai')
        time.sleep(5)
        previous_entry = Executed_Stratergy.objects.filter(
            datetime__year=self.datetime.year,
            datetime__month=self.datetime.month,
            datetime__day=self.datetime.day,
            datetime__hour=self.datetime.hour,
            datetime__minute=self.datetime.minute
        ).exists()
        # If no entry exists for the same minute, save the current entry
        if not previous_entry:
            self.url = Stratergy_settings.objects.all().first().url
            self.response = '200'
            super().save(*args, **kwargs)
            thread = Thread(target=Placed,args=(self,))
            thread.start()
    def __str__(self):
        return f'{self.remark}'


def Placed(self):
    data = json.loads(json.dumps(self.syntax_used))
    url = self.url
    response = requests.post(url,data)
