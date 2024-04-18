from django.contrib import admin
from django.urls import path
from category.views import createCategoryView


urlpatterns = [
    
    path('create/<slug:owner_name>/', createCategoryView, name = 'create_category'),
    
]


