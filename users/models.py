from django.db import models
from adminWorks.models import Blog

# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    print("THis is models")
    print(name)
    print(email)
    print(password)


class Likes(models.Model):
    blogId = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='id')
    email = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email')
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)
    neutral = models.BooleanField(default=True)



