import mimetypes, random, string, json
from django.http import FileResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from .forms import ProductForm, ProductUpdateForm, ProductAttachmentInlineFormSet
from .models import Product, ProductAttachment
from django.contrib.auth.decorators import login_required
from dalle.models import DalleImage
from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from urllib.parse import unquote
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework import status

def product_list_view(request):
    products_list = Product.objects.all()
    return render(request, 'products/list.html', {"products_list":products_list})

@login_required
def product_manage_detail_view(request, handle=None):
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

def product_detail_view(request, handle=None):
    product = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=product)
    is_purchased = False
    if request.user.is_authenticated:
        is_purchased = request.user.purchase_set.all().filter(product=product, completed=True).exists()
    context = {"object": product, "is_purchased": is_purchased, "attachments":attachments}
    return render(request, 'products/detail.html', context)

@login_required
def product_attachment_download_view(request, handle=None, pk=None):
    attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
    can_download = attachment.is_free or False
    if request.user.is_authenticated:
        can_download = True
    if can_download is False:
        return HttpResponseBadRequest()
    file = attachment.file.open(mode='rb')
    filename = attachment.file.name
    content_type, encoding = mimetypes.guess_type(filename)
    response = FileResponse(file)
    response['Content-Type'] = content_type or 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename={filename}'
    return response

@login_required
@api_view(['POST'])
def products_create(request):
    if request.method == 'POST':
        phrase = unquote(request.data.get('phrase'))
        id = request.data.get('id')
        handle=request.data.get('handle')
        dalle_image = get_object_or_404(DalleImage, id=id)
        price = 9.99

        product = Product.objects.create(
            image=dalle_image.ai_image,
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
def product_delete_view(request, handle):
    product = get_object_or_404(Product, handle=handle)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=204)
    context = {'product': product}
    return render(request, 'products/delete.html', context)