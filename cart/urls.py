from django.urls import path
from cart.views import *

urlpatterns = [
  path('', cart, name = 'cart'),
  path('add_cart/<int:product_id>/', add_cart, name = 'add_cart'),
  path('add_cart_item/<int:product_id>/', add_cart_cart, name = 'add_cart_cart'),
  path('remove_cart/<int:product_id>/<int:cart_item_id>/', remove_cart, name = 'remove_cart'),
  
  path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', remove_cart_item, name = 'remove_cart_item'),
  path('checkout/<int:coupon>/', checkOutView, name = 'checkout'),
  path('add_detail_cart/<int:product_id>/', add_product_detail_cart, name = 'add_product_detail_cart'),
  
  path('remove_detail_cart/<int:product_id>/<int:cart_item_id>/', remove_product_detail_cart, name = 'remove_product_detail_cart'),
  path('store_cart/<int:product_id>/', store_cart, name= 'store_cart'),
]
