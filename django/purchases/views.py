from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Purchase
from django.urls import reverse
import stripe
from core.env import config
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY

@login_required
def purchase_start_view(request):
    BASE_ENDPOINT = f'http://{request.get_host()}'
    
    if not request.method == "POST":
        return HttpResponseBadRequest()
    if not request.user.is_authenticated:
        return HttpResponseBadRequest()
    
    handle = request.POST.get("handle")
    product = Product.objects.get(handle=handle)
    stripe_price_id = product.stripe_price_id
    if stripe_price_id is None:
        return HttpResponseBadRequest()
    
    purchase = Purchase.objects.create(user=request.user, product=product)
    request.session['purchase_id'] = purchase.id
    
    success_path = reverse("purchases:success")
    if not success_path.startswith("/"):
        success_path = f"/{success_path}"
    
    stopped_path = reverse("purchases:stopped")
    if not stopped_path.startswith("/"):
        stopped_path = f"/{stopped_path}"

    success_url = f"{BASE_ENDPOINT}{success_path}"
    stopped_url = f"{BASE_ENDPOINT}{stopped_path}"

    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price": stripe_price_id,
                "quantity":1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=stopped_url
    )
    purchase.stripe_checkout_session_id = checkout_session.id
    purchase.stripe_price = product.price
    purchase.save()
    return HttpResponseRedirect(checkout_session.url)

@login_required
def purchase_success_view(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.completed = True
        purchase.save()
        del request.session['purchase_id']
        return HttpResponseRedirect(purchase.product.get_absolute_url())
    return HttpResponse(f"Finished{purchase_id}")

@login_required
def purchase_stopped_view(request):
    purchase_id = request.session.get("purchase_id")
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        del request.session['purchase_id']
        return HttpResponseRedirect(purchase.product.get_absolute_url())
    return HttpResponse("Stopped")

@login_required
def purchase_list_view(request):
    purchases = Purchase.objects.filter(completed=True)
    return render(request, "purchases/list.html", {"purchases": purchases})

@login_required
def purchase_myorder_view(request):
    purchases = Purchase.objects.filter(user=request.user, completed=True)
    return render(request, "purchases/my-order.html", {"purchases": purchases})

@login_required
def purchase_cancel_view(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user, completed=True)
    if request.method == 'POST':
        purchase.completed = False
        purchase.save()
        
    return redirect('purchases:my-orders')
    
