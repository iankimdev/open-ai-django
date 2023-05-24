from django.urls import path
from django.views.generic import TemplateView
from .views import generate_image_from_txt, download_image, generate_image_from_txt_for_custom

app_name = 'dalle'

urlpatterns = [
    path('', generate_image_from_txt, name='dalle'),
    path('custom', generate_image_from_txt_for_custom, name='custom'),
    path("download/<int:image_id>/", download_image, name="download_image"),
]