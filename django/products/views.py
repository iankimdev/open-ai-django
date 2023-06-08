import mimetypes, random, string, json
from django.http import FileResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from .forms import ProductForm, ProductUpdateForm, ProductAttachmentInlineFormSet
from .models import Product, ProductAttachment
from django.contrib.auth.decorators import login_required
from dalle.models import DalleImage
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.parse import unquote
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.exceptions import ValidationError
from core.storages.utils import generate_presigned_url

def products_list(request):
    products_list = Product.objects.all()
    return render(request, 'products/list.html', {"products_list":products_list})

@login_required
@api_view(['POST'])
def products_create(request):
    if request.method == 'POST':
        phrase = unquote(request.data.get('phrase'))
        id = request.data.get('id')
        handle=request.data.get('handle')
        dalle_image = get_object_or_404(DalleImage, id=id)
        price = 9.99
         # Validate handle length      
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
    attachments = ProductAttachment.objects.filter(product=product)
    is_purchased = False
    if request.user.is_authenticated:
        is_purchased = request.user.purchase_set.all().filter(product=product, completed=True).exists()
    context = {"object": product, "is_purchased": is_purchased, "attachments":attachments}
    return render(request, 'products/detail.html', context)

@login_required
def products_update(request, handle=None):
    product = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=product)
    is_manager = False
    if request.user.is_authenticated:
        is_manager = product.user == request.user
    context = {"object": product, "is_manager": is_manager}  # Add "handle" to the context
    if not is_manager:
        return HttpResponseBadRequest()
    
    form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=product)
    attachments = ProductAttachment.objects.filter(product=product)
    formset = ProductAttachmentInlineFormSet(request.POST or None, request.FILES or None, queryset=attachments)
    
    # Product
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.save()
        formset.save(commit=False)
        
        # Product - ProductAttachment
        for _form in formset:
            is_delete = _form.cleaned_data.get("DELETE")
            try:
                attachment_obj = _form.save(commit=False)
            except:
                attachment_obj = None
            if is_delete:
                if attachment_obj is not None:
                    if attachment_obj.pk:
                        attachment_obj.delete()
            else:
                if attachment_obj is not None:
                    attachment_obj.product = instance
                    attachment_obj.save()
        return redirect(product.get_manage_url())

    context['form'] = form
    context['formset'] = formset
    return render(request, 'products/manager.html', context)

@login_required
def product_attachment_download(request, handle=None, pk=None):
    attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
    can_download = attachment.is_free or False
    if request.user.is_authenticated and can_download is False:
        can_download = request.user.purchase_set.all().filter(product=attachment.product, completed=True).exists()
    if can_download is False:
        return HttpResponseBadRequest()
    
    file_name = attachment.file.name # .open(mode='rb') # cdn -> S3 object storage
    file_url = generate_presigned_url(file_name)
    return HttpResponseRedirect(file_url)