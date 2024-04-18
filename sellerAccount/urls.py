from django.contrib import admin
from django.urls import path
from sellerAccount.views import *
from category.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', sellerAccountView, name='seller_signup'),
    path('active/<uid>/', confirmEmail, name='active'),
    path('login/', sellerLogin, name='seller_login'),
    path('category/<slug:owner_name>/', categoryShow, name='category_list'),
    path('product-list/<slug:owner_name>/', productList, name='seller_info'),
    path('dashboard/<slug:owner_name>/', sellerDashboard, name='dashboard'),
    path('add-product/<slug:owner_name>/', addProduct, name='add_product'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
