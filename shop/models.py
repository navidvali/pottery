from datetime import datetime
from django.db import models
from .validators import *


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=35, null=False, unique=True)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.)
    main_image = models.FileField(upload_to='shop/images')
    created_on = models.DateTimeField(blank=True, default=datetime.now)

    class Meta:
        db_table = 'Products'


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=20, null=True, blank=True)
    created_on = models.DateTimeField(blank=True, default=datetime.now)

    class Meta:
        db_table = 'Category'


class ProductsCategory(models.Model):
    productscategory_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    created_on = models.DateTimeField(blank=True, default=datetime.now)

    class Meta:
        db_table = 'ProductsCategory'


class Pictures(models.Model):
    picture_id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to='shop/images')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE)
    created_on = models.DateTimeField(blank=True, default=datetime.now)

    class Meta:
        db_table = 'Pictures'
