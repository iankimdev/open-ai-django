from django.urls import path
from django.views.generic import TemplateView
from .views import generate_image_from_txt
app_name = 'dalle_images'
urlpatterns = [
    path('', generate_image_from_txt, name='generate_image_from_txt'),
]