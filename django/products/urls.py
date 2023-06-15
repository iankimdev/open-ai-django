from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('', views.products_list, name="list"),
    path('order/', views.products_create, name='order'),
    path('<slug:handle>/', views.products_detail, name='detail'),
    path('<slug:handle>/delete/', views.products_delete, name='delete'),
]