from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

import random
from users.urls import *
#validate file extension in add product
from .validators import *

#pagination
from django.core.paginator import Paginator

from .models import *
from .forms import *
from .serializers import *

from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .serializers import ProductsSerializer

from users.models import *


def index(request):
    return render(request, 'index.html')


def shop(request):
    p = Paginator(Products.objects.order_by("-created_on"), 6)
    page = request.GET.get('page')
    products_paginated = p.get_page(page)

    categories = Category.objects.all()
    categories_list = []

    # to show the num of category
    for c in categories:
        num_of_category = len(ProductsCategory.objects.filter(category=c.category_id))
        c = model_to_dict(c)
        c["number"] = num_of_category
        categories_list.append(c)

    num_of_orders = 0
    if request.user.is_authenticated:
        users_orders = UserProduct_Cart.objects.filter(user=request.user, stat="in_cart")
        num_of_orders = len(users_orders)

    unavailable = False
    if not categories:
        unavailable = True
    data = {
        'products_paginated': products_paginated,
        'categories': categories_list,
        'unavailable': unavailable,
        'num_of_orders': num_of_orders,
    }

    return render(request, 'shop.html', data)


def search_product(request):

    search_input = request.GET.get("searchInput")
    print("=================",search_input)

    product = Products.objects.filter(name__icontains=search_input).values()

    return JsonResponse({"product":list(product)})


def category_filter(request):
    category_asked = request.GET.getlist("SelectedCategories[]")
    filtered_products = []
    for c in category_asked:
        productscategory = ProductsCategory.objects.filter(category=c)
        for p in productscategory:
            product = ProductsSerializer(p.product).data
            product['product_id'] = p.product.product_id
            if product in filtered_products:
                continue
            else:
                filtered_products.append(product)

    return JsonResponse({"filtered_products": filtered_products})


def check_category(category):
    already_added = False
    added_category = Category.objects.all()
    i = 0
    cat_list = []
    for item in added_category:
        temp = added_category[i].category
        cat_list.append(temp)
        i += 1
    
    if category in cat_list:
        already_added = True

    return already_added


def add_product(request):
    if not request.user.is_staff:
        return render(request, "users/access_denied.html")
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        pictures_form = PicturesForm(request.POST, request.FILES)
        category_list = request.POST.getlist("category")
        if product_form.is_valid() and validate_file_extension(request.FILES.get("main_image")):
            try:
                product = product_form.save()
                if len(category_list) > 0:
                    for i in category_list:
                        if check_category(i):
                            category = Category.objects.get(category=i)
                            ProductsCategory.objects.create(category=category, product=product)
                        else:
                            category = Category.objects.create(category=i)
                            ProductsCategory.objects.create(category=category, product=product)
                if pictures_form:
                        for image in request.FILES.getlist("image"):
                            if validate_file_extension(image):
                                Pictures.objects.create(image=image, product=product)
                            else:
                                error = {"error": "invalid extra picture extension"}
                                return render(request, 'add_product.html', error)
                return redirect(admin_panel)
            except Exception as e:
                print(e)
        else:
            print("++++++++++++++++++++",product_form.errors)
            error = {"error":"invalid product info"}
            return render(request, 'add_product.html', error)
    else:
        product_form = ProductForm()
        pictures_form = PicturesForm()
        category_form = CategoryForm()
        unavailable = False
        added_categorys = Category.objects.order_by("-created_on")
        if not added_categorys:
            unavailable = True
        data = {
            'product_form': product_form,
            'pictures_form': pictures_form,
            'category_form': category_form,
            'added_categorys': added_categorys,
            'unavailable': unavailable,
         }

    return render(request, 'add_product.html', data)


def view_product(request, product_id):

    product = Products.objects.get(product_id=product_id)
    try:
        if request.user.is_authenticated:
            users_orders_num = UserProduct_Cart.objects.get(product=product, user=request.user, stat="in_cart")
        else:
            users_orders_num = 0
    except UserProduct_Cart.DoesNotExist:
        users_orders_num = 0
    images = Pictures.objects.filter(product=product)
    category = ProductsCategory.objects.filter(product=product)
    
    num_of_all_orders = 0
    if request.user.is_authenticated:
        users_orders = UserProduct_Cart.objects.filter(user=request.user, stat="in_cart")
        num_of_all_orders = len(users_orders)

    data = {
        'product': product,
        'category': category,
        'images': images,
        "users_orders_num": users_orders_num,
        "num_of_all_orders": num_of_all_orders,
    }
    return render(request, 'view_product.html', data)


