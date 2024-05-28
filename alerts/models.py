from django.db import models
from trade.models import status,webhookurl

# Create your models here.
class orders(models.Model):
    id=models.AutoField(primary_key=True)
    datetime = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100)
    webhook=models.ForeignKey(webhookurl,on_delete=models.CASCADE)
    syntax = models.TextField()
    status = models.CharField(choices=status, max_length=12,default="initiated")
    class Meta:
         verbose_name = "Order"
         verbose_name_plural = "Orders"
    def __str__(self):
       return self.name
    
class IndexTokens(models.Model):
    BANKNIFTY = models.CharField(max_length=100)
    CRUDEOIL = models.CharField(max_length=100)
    SENSEX = models.CharField(max_length=100)
    NIFTY = models.CharField(max_length=100)
    FIN_NIFTY = models.CharField(max_length=100,default='100')
    BANKEX = models.CharField(max_length=100,default='100')
    class Meta:
         verbose_name = "Index Token Number"
         verbose_name_plural = "Index Tokens"
    def __str__(self):
       return 'Index Tokens'

