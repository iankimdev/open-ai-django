from django.urls import path
from . import views

app_name='purchases'

urlpatterns = [
    path('start/', views.purchase_start_view, name="start"),
    path('success/', views.purchase_success_view, name='success'),
    path('stopped/', views.purchase_stopped_view, name='stopped'),
    path('list/', views.purchase_list_view, name='list'),
    path('my-orders/', views.purchase_myorder_view, name='my-orders'),
    path('cancel/<int:purchase_id>/', views.purchase_cancel_view, name='my-order-cancel'),
]