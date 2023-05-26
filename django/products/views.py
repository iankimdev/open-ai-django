import mimetypes

from django.http import FileResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from .forms import ProductForm, ProductUpdateForm, ProductAttachmentInlineFormSet
from .models import Product, ProductAttachment
from django.contrib.auth.decorators import login_required
from dalle.models import DalleImage
@login_required
def product_create_view(request):
    context = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user
            obj.save()
            return redirect(obj.get_manage_url())
        # else:
        form.add_error(None, "User must be logged in") 
    context['form'] = form
    return render(request, 'products/create.html', context)

def product_list_view(request):
    object_list = Product.objects.all()
    return render(request, 'products/list.html', {"object_list":object_list})

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

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})



import random
import string
def generate_handle():
    # Generate a random alphanumeric handle
    letters_digits = string.ascii_letters + string.digits
    handle = ''.join(random.choice(letters_digits) for _ in range(8))
    return handle
from urllib.parse import unquote
@login_required
def custom_order_view(request, phrase, id):
    if request.method == 'POST':
        phrase = unquote(phrase)
        print(phrase)
        id = id

        # Retrieve the DalleImage object
        dalle_image = get_object_or_404(DalleImage, id=id)

        # Create the Product object
        handle = generate_handle()  # Generate handle automatically
        price = 9.99

        product = Product.objects.create(
            image=dalle_image.ai_image,
            name=phrase,
            handle=handle,
            price=price
        )
        context = {
            'product': product
        }
        return HttpResponseRedirect(product.get_absolute_url())
    else:
        return HttpResponseBadRequest("Invalid request method.")

@login_required
def product_delete_view(request, handle):
    product = get_object_or_404(Product, handle=handle)
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    if request.method == 'POST':
        product.delete()
        return redirect('products:list')
    
    context = {'product': product}
    return render(request, 'products/delete.html', context)