from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
# Create your views here.
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Purchase
from django.urls import reverse
import stripe
from core.env import config
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default=None)
stripe.api_key = STRIPE_SECRET_KEY
BASE_ENDPOINT = "http://127.0.0.1:8000"

@login_required
def purchase_start_view(request):
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
    
    cancel_path = reverse("purchases:cancel")
    if not cancel_path.startswith("/"):
        cancel_path = f"/{cancel_path}"

    success_url = f"{BASE_ENDPOINT}{success_path}"
    cancel_url = f"{BASE_ENDPOINT}{cancel_path}"

    checkout_session = stripe.checkout.Session.create(
        line_items = [
            {
                "price": stripe_price_id,
                "quantity":1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url
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
    purchases = Purchase.objects.all()
    return render(request, "purchases/list.html", {"purchases": purchases})
