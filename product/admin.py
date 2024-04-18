from django.contrib import admin
from product.models import Product, Size

class ProductAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('product_name',)}
  list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')

admin.site.register(Product, ProductAdmin)
admin.site.register(Size)


