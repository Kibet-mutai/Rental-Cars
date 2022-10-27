from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
# Create your models here.



class Car(models.Model):
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    capacity = models.CharField(max_length=50)
    description = models.CharField(max_length=350)
    image = models.ImageField(upload_to='images',null=True)
    city = models.CharField(max_length=50,null=True)
    availability = models.BooleanField(null=True)
    rates_per_day = models.IntegerField(null=True)



class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE,null=True)
    hire_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(default=timezone.now)
