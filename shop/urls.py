from django.urls import path
from .views import *


urlpatterns = [
    path('', shop, name='shop'),
    path('category_filter/', category_filter, name='category_filter'),
    path('search_product/', search_product, name='search_product'),
    path('index/', index, name='index'),
    path('add_product/', add_product, name='add_product'),
    path('view_product/<int:product_id>', view_product, name='view_product')
]
