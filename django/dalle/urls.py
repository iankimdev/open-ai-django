from django.urls import path
from django.views.generic import TemplateView
from .views import download_image, generate_image_from_txt_for_custom

app_name = 'dalle'

urlpatterns = [
    path('custom', generate_image_from_txt_for_custom, name='custom'),
    path("download/<int:image_id>/", download_image, name="download_image"),
]