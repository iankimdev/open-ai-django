from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup, signin, signout, profile
from users.views import ChangePasswordView

app_name = 'users'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('profile/', profile, name='profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]
