from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

from shop.models import *


class Coupons(models.Model):
    coupon = models.AutoField(primary_key=True)
    coupon_code = models.CharField(max_length=35, null=False, unique=True)
    percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_on = models.DateTimeField(blank=True, default=datetime.now)


class Orders(models.Model):
    order = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    payment_method_choices = [("online", 'online'), ("on_delivery", 'on delivery')]
    payment_method = models.CharField(max_length=20, choices=payment_method_choices, default="online")
    payment_stat_choices = [("done_online", 'done online'), ("done_on_delivery", 'done on delivery'), ("not_payed", "not payed")]
    payment_stat = models.CharField(max_length=20, choices=payment_stat_choices, default="not_payed")
    total = models.DecimalField(max_digits=50, decimal_places=2)
    used_coupon = models.ForeignKey(to=Coupons, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)
    order_stat_choices = [("delivered", 'delivered'), ("in_line_for_delivery", 'in line for delivery'),]
    order_stat = models.CharField(max_length=30, choices=order_stat_choices, null=True)
    address = models.TextField()
    created_on = models.DateTimeField(blank=True, default=datetime.now)


class AccountDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()


class UserProduct_Cart(models.Model):
    UserProduct_Cart = models.AutoField(primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    order = models.ForeignKey(to=Orders, on_delete=models.CASCADE, null=True)
    stat_choices = [("in_cart", 'in cart'), ("in_order", 'in order')]
    stat = models.CharField(max_length=20, choices=stat_choices, default="in_cart")
    created_on = models.DateTimeField(blank=True, default=datetime.now)


