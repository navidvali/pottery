from django.urls import path, include
from .views import *


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('admin_panel_products/', admin_panel_products, name='admin_panel_products'),
    path('admin_panel_delete/', admin_panel_delete, name='admin_panel_delete'),
    path('admin_panel_edit/<int:product_id>', admin_panel_edit, name='admin_panel_edit'),
    path('register/', register, name='register'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('delete_order/', delete_order, name='delete_order'),
    path('check_coupon/', check_coupon, name='check_coupon'),
    path('add_coupon/', add_coupon, name='add_coupon'),
    path('set_pre_order/', set_pre_order, name='set_pre_order'),
    path('set_order/<int:order_id>', set_order, name='set_order'),
    path('complete_order/<int:order_id>', complete_order, name='complete_order'),
    path('delete_ongoing_order/<int:order_id>', delete_ongoing_order, name='delete_ongoing_order'),
    path('fake_pay/<int:order_id>', fake_pay, name='fake_pay'),
    path('thanks/', thanks, name='thanks'),
    path('receipt/', receipt, name='receipt'),
    path('edit_address/', edit_address, name='edit_address'),
    path('profile/', profile, name='profile'),
    path('view_all_orders/', view_all_orders, name='view_all_orders'),
]
