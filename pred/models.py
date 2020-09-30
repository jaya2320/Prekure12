from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Report(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    radius = models.CharField(max_length=100)
    texture = models.CharField(max_length=100)
    perimeter = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    smoothness = models.CharField(max_length=100)
    result= models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    experience = models.IntegerField()
    area = models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    phone_number=models.BigIntegerField()
    fees = models.IntegerField()
    img=models.ImageField(upload_to="media1")




