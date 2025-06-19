from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

