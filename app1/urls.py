from django.contrib import admin
from django.urls import path, include
# AGREGAR URLS DE APPL
from app1 import views

urlpatterns = [

    path('', views.saludar, name='home'),       
    path('info/', views.info, name='info'),     
    path('stores/', views.Stores_view, name='stores'),
    path('products/', views.Products_view, name='products'),
    path('create_store/', views.create_store, name='create_store'),
    path('create_product/', views.create_product, name='create_product'),
    path('details/<int:id>', views.details, name='details'),
    path('contact',views.contact, name='contact'),
]