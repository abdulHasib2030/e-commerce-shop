from django.contrib import admin
from cart.models import *
# Register your models here.
class CartAdmin(admin.ModelAdmin):
  list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
  list_display = ('product', 'cart', 'quantity', 'is_active')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(BillingDetails)
admin.site.register(FirstOrderCoupon)
admin.site.register(Order)
