import stripe
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from core.env import config

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    stripe_product_id = models.CharField(max_length=220, blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    name = models.CharField(max_length=200)
    handle = models.SlugField(unique=True, max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    og_price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    stripe_price_id = models.CharField(max_length=220, blank=True, null=True)
    stripe_price = models.IntegerField(default=999) # 100 * price
    price_changed_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    @property
    def display_name(self):
        return self.name
    @property
    def display_price(self):
        return self.price
    
    def get_image_url(self):
        if self.image:
            return self.image
        return ''
    
    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if self.name:
            stripe_product_r = stripe.Product.create(name=self.name)
            self.stripe_product_id = stripe_product_r.id
        
        if not self.stripe_price_id:
            stripe_price_obj = stripe.Price.create(
                    product = self.stripe_product_id,
                    unit_amount=self.stripe_price,
                    currency="usd",
                )
            self.stripe_price_id = stripe_price_obj.id
        
        # tracking price changed
        if self.price != self.og_price: 
            self.og_price = self.price
            self.stripe_price = int(self.price * 100)
            if self.stripe_product_id:
                stripe_price_obj = stripe.Price.create(
                    product = self.stripe_product_id,
                    unit_amount=self.stripe_price,
                    currency="usd",
                )
                self.stripe_price_id = stripe_price_obj.id
            self.price_changed_timestamp = timezone.now()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"handle": self.handle})