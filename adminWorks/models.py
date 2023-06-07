from django.db import models

# Create your models here.
class Admin(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    print("THis is models")
    print(name)
    print(email)
    print(password)

class Blog(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField(default='hi')
    likeCount =  models.IntegerField(default=0)
    dislikeCount = models.IntegerField(default=0)

