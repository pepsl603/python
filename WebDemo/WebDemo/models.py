from django.db import models

# Create your models here.

class Test(models.Model):
    name = models.CharField(max_length= 200)
    recdate = models.DateTimeField(auto_now=True)
