from django.db import models
from user.models import UserRegister


class AdminData(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    image = models.ImageField(upload_to='admin_profile/')
    password = models.CharField(max_length=8)


class Complains(models.Model):
    name = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    description = models.TextField(max_length=4000)


class Products(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
    p_status = models.CharField(max_length=20)
    bid_price = models.FloatField()
    image1 = models.ImageField(upload_to='products/')
    image2 = models.ImageField(upload_to='products/')
    image3 = models.ImageField(upload_to='products/')
    disc = models.TextField(max_length=3000)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)


class BitTable(models.Model):
    bid = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)


class MaxBidTable(models.Model):
    mid = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    max_amount = models.FloatField()


class Order(models.Model):
    o_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    o_status = models.CharField(max_length=20)
    final_price = models.FloatField()


class CheckoutData(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    contact = models.IntegerField()
    status = models.CharField(max_length=20)
    add = models.CharField(max_length=100)
    add2 = models.CharField(max_length=100)
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    pin = models.IntegerField()


