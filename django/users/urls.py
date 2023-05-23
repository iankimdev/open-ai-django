from django.urls import path
from .views import signup

urlpatterns = [
    # 다른 URL 패턴들...
    path('', signup, name='signup'),
]
