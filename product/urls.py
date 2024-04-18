from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from product.views import *

urlpatterns = [
    path('', store, name= 'store'),
    path('products_by_category/<int:id>/', store, name='products_by_category'),
    path('products_by_prize/<int:price>/', store, name='products_by_prize'),
    path('<slug:category_slug>/<slug:product_slug>/', Product_detail, name = 'product_detail'),
    path('search/', search, name = 'search'),
    path('review/', ProductReview, name = 'product')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
