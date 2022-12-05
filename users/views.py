from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError 
from django.core.paginator import Paginator

from .serializers import *
from shop.models import *
from shop.forms import *
from shop.validators import *
from shop.serializers import *

from .forms import *
from .models import *


def dashboard(request):
    return render(request, "users/dashboard.html")


def admin_panel(request):

    coupons = Coupons.objects.all()
    products = Products.objects.all().order_by('-created_on')
    
    data = {
        "coupons": coupons,
        "products": products,
    }

    return render(request, "users/admin_panel.html", data)


def admin_panel_products(request):

    products = Products.objects.order_by('-created_on')
    productsserialized = ProductsSerializer(products, many=True).data
    return JsonResponse({"products": productsserialized})


def admin_panel_delete(request):

    pk = request.GET.get("product_id")
    products = Products.objects.get(pk=pk).delete()

    data = {
        "deleted": True,
    }

    return JsonResponse(data)


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


def admin_panel_edit(request, product_id):
    if request.method == "POST":

        product = Products.objects.get(pk=product_id)
        pictures = Pictures.objects.filter(product=product_id)
        products_categories = ProductsCategory.objects.filter(product=product)

        product_form = ProductForm(request.POST, request.FILES, instance=product)

        category_list = request.POST.getlist("category")

        if product_form.is_valid():
            if request.FILES.get("main_image"):
                if validate_file_extension(request.FILES.get("main_image")):
                    product_form.save()
                else:
                    error = {"error":"invalid product info"}
                    return render(request, 'users/admin_panel_edit.html', error)

            else:
                product_form.save()

        if request.FILES.getlist("image"):
            if pictures:
                for pic in pictures:
                    pic.delete()
            for pic in request.FILES.getlist("image"):
                if validate_file_extension(pic):
                    Pictures.objects.create(image=pic, product=product)
                else:
                    error = {"error": "invalid extra picture extension"}
                    return render(request, 'users/admin_panel_edit.html', error)

        if products_categories:
            for cat in products_categories:
                cat.delete()
        for cat in category_list:
            if check_category(cat):
                category = Category.objects.get(category=cat)
                ProductsCategory.objects.create(category=category, product=product)
            else:
                category = Category.objects.create(category=cat)
                ProductsCategory.objects.create(category=category, product=product)

        return redirect(admin_panel)
 
    if request.method == "GET":

        product = Products.objects.get(product_id=product_id)
        finalcategorys = []

        all_categories = Category.objects.all()
        productcategoryslist = []
        productcategorys = ProductsCategory.objects.filter(product=product_id)
        for c in productcategorys:
            productcategoryslist.append(c.category)

        for cat in all_categories:
            if cat in productcategoryslist:
                cat_dict = model_to_dict(cat)
                cat_dict['has_category'] = True
                finalcategorys.append(cat_dict)
            else:
                finalcategorys.append(cat)

        pictures = Pictures.objects.filter(product=product_id)
        for picture in pictures:
            picture.name = str(picture.image).strip("/shop/images/-")

        data = {
            "product" : product,
            "categorys": finalcategorys,
            "pictures": pictures,
        }

        return render(request, "users/admin_panel_edit.html", data)

def register(request):
    if request.method == "POST":
        custom_register = CustomRegister(request.POST)
        account_details_form = AccountDetailsForm(request.POST)

        try:
            if custom_register.is_valid():
                custom_register_instance = custom_register.save()
                AccountDetails.objects.create(user=custom_register_instance, address=request.POST.get("address"))
                login(request, custom_register_instance)
                return redirect("shop") 
            else:
                messages.error(request, custom_register.errors)
                return render(request, "registration/register.html") 
        except Exception as e:
            print(e)
    if request.method == "GET":
        custom_register = CustomRegister()
        account_details_form = AccountDetailsForm()

        data = {
            "custom_register":custom_register,
            "account_details_form":account_details_form,
        }
        return render(request, "registration/register.html", data) 
    # return HttpResponse(status=204)

@login_required(login_url='/users/accounts/login/')
def cart(request):
    if request.method == "GET":
        products_in_cart = UserProduct_Cart.objects.filter(user=request.user, stat="in_cart")
        total_price = 0
        for pro in products_in_cart:
            total_price += pro.product.price
        users_address = AccountDetails.objects.get(user=request.user).address
        try:
            ongoing_order_id = False
            ongoing_order_id = Orders.objects.get(user=request.user, order_stat=None).order
            users_order = Orders.objects.filter(user=request.user,)
            for i in users_order:
                if i.order_stat in ['in_line_for_delivery', 'delivered']:
                    has_ordered = False
                else:
                    has_ordered = True
        except ObjectDoesNotExist:
            has_ordered = False
        data = {
            "products_in_cart": products_in_cart,
            "users_address": users_address,
            "total_price": total_price,
            "has_ordered": has_ordered,
            "ongoing_order_id": ongoing_order_id,
        }

        return render(request, "users/cart.html", data)

@login_required(login_url='/users/accounts/login/')
def add_to_cart(request):

    product_id = request.GET.get("product_id")
    product = Products.objects.get(product_id=product_id)
    user = request.user

    try:
        users_orders = UserProduct_Cart.objects.filter(user=user, stat="in_cart")
        exists = False
        for user_order in users_orders:
            if str(product_id) == str(user_order.product.product_id):
                user_order.number += 1
                user_order.save()
                exists = True

        if not exists:
            UserProduct_Cart.objects.create(user=user, product=product)
    except Exception as e:
        print(e)

    return JsonResponse({"job": "done"})

@login_required(login_url='/users/accounts/login/')
def delete_order(request):
    productuser_id = request.GET.get("productuser_id")
    object = UserProduct_Cart.objects.get(UserProduct_Cart=productuser_id)
    object.delete()

    return JsonResponse({"job": "done"})

@login_required(login_url='/users/accounts/login/')
def check_coupon(request):
    entered_coupon = request.GET.get("entered_coupon")
    total = request.GET.get("total")
    percent = 100


    try:
        coupon = Coupons.objects.get(coupon_code=entered_coupon)
        if coupon:
            #  if coupon.valid_num_of_use >= 1:
            stat = True
            percent = int(coupon.percent)
            x = 100 - percent
            total = abs(float(total)*x/100)
            couponserialized = CouponsSerializers(coupon).data
            #  else:
            #      couponserialized = "this coupon is used out!"
            #      stat = "-1"
    except ObjectDoesNotExist:
        couponserialized = "invalid coupon!"
        stat = "-2"

    data = {
        "total": total,
        "percent": percent,
        "coupon": couponserialized,
        "stat": stat,
    }

    return JsonResponse(data)

@login_required(login_url='/users/accounts/login/')
def add_coupon(request):
    if request.method == "GET":
        couponsform = CouponsForm()

        data = {
            "couponsform": couponsform,
        }
    if request.method == "POST":
        couponsform = CouponsForm(request.POST)

        if couponsform.is_valid():
            try:
                couponsform.save()
            except Exception as e:
                print(e)

        return redirect(admin_panel)

    return render(request, "users/add_coupon.html", data)

@login_required(login_url='/users/accounts/login/')
def set_pre_order(request):
        order_exists = False
        try:
            users_order = Orders.objects.filter(user=request.user,)
            for i in users_order:
                if i.order_stat in ['in_line_for_delivery','delivered']:
                    order_exists = False
                else:
                    order_exists = True
        except ObjectDoesNotExist:
            order_exists = False
        if not order_exists:
            orders_payment_method = request.GET.get("payment_method")
            total = 0
            products_in_cart = UserProduct_Cart.objects.filter(user=request.user, stat="in_cart")
            address = AccountDetails.objects.get(user=request.user).address
            for i in products_in_cart:
                total += i.product.price
            order = Orders.objects.create(
                user=request.user,
                payment_method=orders_payment_method,
                total=total,
                address=address,
            )
            for i in products_in_cart:
                i.stat = "in_order"
                i.order = order
                i.save()
            return JsonResponse({
                "redirect": "set_order",
                "order": order.order,
            })
        else:
            return JsonResponse({"error": "you can only have one ongoing order"})

        return redirect("cart")


@login_required(login_url='/users/accounts/login/')
def set_order(request, order_id):
    if request.method == "GET":
        users_order_details = Orders.objects.get(user=request.user, order=order_id)
        users_order_products = UserProduct_Cart.objects.filter(user=request.user, order=order_id)
        address = AccountDetails.objects.get(user=request.user).address

        data = {
            "users_order_details": users_order_details,
            "users_order_products": users_order_products,
            "address": address,
            "order": order_id,
        }

        return render(request, "users/set_order.html", data)
    else:
        users_order_details = Orders.objects.get(user=request.user)
        users_order_details.description = request.POST.get("description")
        if request.POST.get("used_coupon"):
            the_used_coupon = Coupons.objects.get(coupon=request.POST.get("used_coupon"))
            # if the_used_coupon.valid_num_of_use >= 1:
            percent = 100 - int(the_used_coupon.percent)
            new_total = request.POST.get("total")*percent/100
            users_order_details.used_coupon = request.POST.get("used_coupon")
            users_order_details.total = new_total

            return JsonResponse({"ok":"ok"})


@login_required(login_url='/users/accounts/login/')
def complete_order(request, order_id):
    if request.method == "GET":
        used_coupon = request.GET.get("coupon")
        try:
            users_order_details = Orders.objects.get(order=order_id)
            if used_coupon:
                users_order_details.total = float(request.GET.get("new_total"))
                users_order_details.used_coupon = Coupons.objects.get(coupon_code=request.GET.get("coupon"))
            description = request.GET.get("description")
            if description:
                users_order_details.description = description
            users_order_details.save()
            if users_order_details.payment_method == "online":
                data = {
                    "redirect": "/users/fake_pay",
                    "pay": "1",
                }
                return JsonResponse(data)
            if users_order_details.payment_method == "on_delivery":
                users_order_details.order_stat = "in_line_for_delivery"
                users_order_details.save()
                data = {
                    "redirect": "/users/thanks",
                    "pay": "2",
                }
                return JsonResponse(data)
        except Exception as e:
            print(e)


@login_required(login_url='/users/accounts/login/')
def delete_ongoing_order(request, order_id):
    users_order_details = Orders.objects.get(order=order_id)
    users_order_details.delete()
    products_in_cart = UserProduct_Cart.objects.filter(user=request.user, stat="in_order",order=users_order_details)
    for i in products_in_cart:
        i.delete()
    return redirect("shop")


@login_required(login_url='/users/accounts/login/')
def fake_pay(request, order_id):
    users_order_details = Orders.objects.get(order=order_id)
    users_order_details.payment_stat = "done_online"
    users_order_details.order_stat = "in_line_for_delivery"
    users_order_details.save()
    return render(request, "users/fake_pay.html")


@login_required(login_url='/users/accounts/login/')
def thanks(request):
    return render(request, "users/thanks.html")


@login_required(login_url='/users/accounts/login/')
def receipt(request):
    users_delivered_orders = Orders.objects.filter(user=request.user, order_stat="delivered")
    users_in_line_orders = Orders.objects.filter(user=request.user, order_stat="in_line_for_delivery")
    data = {
        "users_delivered_orders": users_delivered_orders,
        "users_in_line_orders": users_in_line_orders,
    }
    return render(request, "users/receipt.html", data)


@login_required(login_url='/users/accounts/login/')
def edit_address(request):
    if request.method == "POST":
        new_address = request.POST.get("address")
        user = AccountDetails.objects.get(user=request.user)
        user.address = new_address
        user.save()
        return redirect('profile')
    else:
        address_form = AccountDetailsForm()
        data = {
            "address_form": address_form,
        }

        return render(request, "users/edit_address.html/", data)


@login_required(login_url='/users/accounts/login/')
def profile(request):
    address = AccountDetails.objects.get(user=request.user).address

    data = {
        "address": address,
    }

    return render(request, "users/profile.html/", data)


def view_all_orders(request):
    o = Paginator(Orders.objects.order_by("-created_on"), 4)
    page = request.GET.get('page')
    orders_paginated = o.get_page(page)

    data = {
        "orders": orders_paginated,
    }

    return render(request, "users/view_all_orders.html/", data)