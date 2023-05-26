from django.urls import path
from . import views

app_name='products'

urlpatterns = [
    path('', views.product_list_view, name="list"),
    path('create/', views.product_create_view, name='create'),
    path('<slug:handle>/', views.product_detail_view, name='detail'),
    path('<slug:handle>/update/', views.product_manage_detail_view, name='update'),
    path('<slug:handle>/download/<int:pk>', views.product_attachment_download_view, name='download'),
    path("order/<path:phrase>/<int:id>", views.custom_order_view, name="custom_order_view"),
    path('<slug:handle>/delete/', views.product_delete_view, name='delete'),
]