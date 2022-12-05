from django.forms import ModelForm, ValidationError
from .models import *


class ProductForm(ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'description', 'main_image']


class PicturesForm(ModelForm):
    class Meta:
        model = Pictures
        fields = ['image']


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category']
