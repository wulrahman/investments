from django.db import models

# importing django core module  
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

# importing requests module  
from requests import get

# importing os.path module  
from os.path import splitext, basename

# importing uuid module  
from uuid import uuid4

def random_file_name(instance, filename):
    base, ext = splitext(filename)
    return "%s%s" % (uuid4(), ext)

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=200, default="")
    logo = models.ImageField(blank=True, upload_to=random_file_name)
    companyName = models.CharField(max_length=200, default="")
    employees = models.CharField(max_length=200, default="",  blank=True)
    exchange = models.CharField(max_length=200, default="",)
    industry = models.CharField(max_length=200, default="", blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    ceo = models.CharField(max_length=200, default="", blank=True)
    securityName = models.CharField(max_length=200, default="", blank=True)
    issueType = models.CharField(max_length=200, default="", blank=True)
    sector = models.CharField(max_length=200, default="", blank=True)
    primarySicCode = models.CharField(max_length=200, default="", blank=True)
    tags = models.CharField(max_length=200, default="", blank=True)
    address	= models.CharField(max_length=200, default="", blank=True)
    address2  = models.CharField(max_length=200, default="", blank=True)
    state = models.CharField(max_length=200, default="", blank=True)
    city = models.CharField(max_length=200, default="", blank=True)
    zip = models.CharField(max_length=200, default="", blank=True)
    country = models.CharField(max_length=200, default="", blank=True)
    phone = models.CharField(max_length=200, default="", blank=True)

    def __str__(self):
        return str(self.symbol)

class Position(models.Model):
    size = models.IntegerField(default=1)
    symbol = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    price = models.CharField(max_length=200, default="")
    open = models.BooleanField(default=True)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.symbol)


class Quote(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    symbol = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    price = models.CharField(max_length=200, default="")

    def __str__(self):
        return str(self.symbol)


class Balance(models.Model):
    json = models.JSONField()
    datetime = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.datetime.strftime('%Y-%m-%d %H:%M')

