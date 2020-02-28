from django.db import models


class UserRegister(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    phone = models.IntegerField(unique=True)
    email = models.EmailField(max_length=30, unique=True)
    status = models.CharField(max_length=10)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=20)
    doj = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='user_profile/')

    def __str__(self):
        return self.name+self.lname

