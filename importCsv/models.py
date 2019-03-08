from django.db import models

# Create your models here.
class City(models.Model):
    abbrev = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Hotel(models.Model):
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    #TODO:
    data = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Url(models.Model):
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=1000)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.url