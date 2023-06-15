from django.urls import path
from .views import generate_image

app_name = 'dalle'

urlpatterns = [
    path('custom/', generate_image, name='custom'),
]