from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    score = models.FloatField(default=0)
    latitude = models.DecimalField(max_digits=16, decimal_places=14)
    longitude = models.DecimalField(max_digits=17, decimal_places=14)

