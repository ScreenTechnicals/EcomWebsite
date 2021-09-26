from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Pizza(models.Model):
    sno = models.AutoField(primary_key=True)
    Pizza_name = models.CharField(max_length=200)
    Pizza_desc = models.CharField(max_length=400)
    Pizza_price = models.FloatField()
    image_url = models.TextField(default="")
    def __str__(self):
        return self.Pizza_name
    

class Orders(models.Model):
    Pizza_name = models.CharField(max_length=200, default="")
    Pizza_desc = models.CharField(max_length=400, default="")
    Pizza_price = models.FloatField(default=0)
    User = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Pizza_name
