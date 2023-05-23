from django.urls import path
from .views import signup, signin

app_name='users'

urlpatterns = [
    # 다른 URL 패턴들...
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
]
