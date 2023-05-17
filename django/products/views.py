import mimetypes

from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from .forms import ProductForm, ProductUpdateForm
from .models import Product, ProductAttachment

def product_create_view(request):
    context = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect('/products/create/')
        # else:
        form.add_error(None, "User must be logged in") 
    context['form'] = form
    return render(request, 'products/create.html', context)

def product_list_view(request):
    object_list = Product.objects.all()
    return render(request, 'products/list.html', {"object_list":object_list})

def product_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_owner = False
    if request.user.is_authenticated:
        is_owner = True
    context = {"object": obj, "is_owner": is_owner, "attachments":attachments}
    return render(request, 'products/detail.html', context)

def product_manage_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    is_manager = False
    if request.user.is_authenticated:
        is_manager = obj.user == request.user
    context = {"object": obj, "is_manager": is_manager}

    if is_manager:
        form = ProductUpdateForm(request.POST or None, request.FILES or None, instance = obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
        context['form'] = form
    return render(request, 'products/detail.html', context)

def product_attachment_download_view(request, handle=None, pk=None):
    #attachment = ProductAttachment.objects.all().first()
    attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
    download_available = attachment.is_free or False
    if request.user.is_authenticated:
        download_available = True
    if download_available is False:
        return HttpResponseBadRequest()
    file = attachment.file.open(mode='rb')
    filename = attachment.file.name
    content_type, encoding = mimetypes.guess_type(filename)
    response = FileResponse(file)
    response['Content-Type'] = content_type or 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename={filename}'
    return response