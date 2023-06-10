from django.urls import path
from .views import signup, signin, signout, profile
from users.views import ChangePasswordView, DeleteUserView

app_name = 'users'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('profile/', profile, name='profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password-change'),
    path('delete/', DeleteUserView.as_view(), name='delete'),
]
