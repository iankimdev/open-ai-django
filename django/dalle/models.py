from django.db import models
from django.urls import reverse

# Create your models here.
class DalleImage(models.Model):
    phrase = models.CharField(max_length=200)
    ai_image = models.ImageField(upload_to='images')

    def __str__(self):
        return str(self.phrase)
    
    def get_download_url(self):
        return reverse("dalle:download_image", args=[self.id])