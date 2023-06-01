from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('', views.product_list, name="list"),
    path('order/', views.products_create, name='order'),
    path('<slug:handle>/', views.product_detail, name='detail'),
    path('<slug:handle>/delete/', views.product_delete, name='delete'),
    
    # NO USE
    path('<slug:handle>/update/', views.product_manage_detail_view, name='update'),
    path('<slug:handle>/download/<int:pk>', views.product_attachment_download_view, name='download'),
    
]