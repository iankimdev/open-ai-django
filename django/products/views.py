from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.contrib.auth.decorators import login_required
from dalle.models import DalleImage
from .models import Product
from rest_framework.response import Response
from urllib.parse import unquote
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import ValidationError

def products_list(request):
    products_list = Product.objects.all()
    
    for product in products_list:
        url = str(product.image)
        url_without_query = url.split('?')[0]
        product.image = url_without_query

    return render(request, 'products/list.html', {"products_list": products_list})

@login_required
@api_view(['POST'])
def products_create(request):
    if request.method == 'POST':
        phrase = unquote(request.data.get('phrase'))
        id = request.data.get('id')
        handle=request.data.get('handle')
        dalle_image = get_object_or_404(DalleImage, id=id)
        price = 9.99
        
        if len(handle) > 255:
            error_message = "Dalle phrase length should be less than or equal to 255 characters."
            raise ValidationError(error_message)
        Product.objects.create(
            image=dalle_image.get_image_url(),
            name=phrase,
            handle=handle,
            price=price,
            id=id
        )
        return Response(status=status.HTTP_201_CREATED)
    else:
        return HttpResponseBadRequest("Invalid request method.")
    
@login_required
@api_view(['GET', 'DELETE'])
def products_delete(request, handle):
    product = get_object_or_404(Product, handle=handle)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=204)
    context = {'product': product}
    return render(request, 'products/delete.html', context)

def products_detail(request, handle=None):
    product = get_object_or_404(Product, handle=handle)

    url = str(product.image)
    url_without_query = url.split('?')[0]
    product.image = url_without_query
    
    is_purchased = False
    if request.user.is_authenticated:
        is_purchased = request.user.purchase_set.all().filter(product=product, completed=True).exists()
    context = {"product": product, "is_purchased": is_purchased}
    return render(request, 'products/detail.html', context)