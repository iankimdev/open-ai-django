from django.contrib import admin
from .models import Product, ProductAttachment

admin.site.register(Product)
admin.site.register(ProductAttachment)