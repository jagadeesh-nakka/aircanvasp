from django.db import models
from django.contrib.auth.models import User
class profilepic(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pic=models.FileField()
    

