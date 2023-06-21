from django.shortcuts import render
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from bookings.forms import BookingForm
from payment.models import UserPayment
from useraccount.models import User
from bookings.models import Booking
import stripe
import time


# Create your views here.
## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get("session_id", None)
    booking_form = BookingForm(request.POST)

    session = stripe.checkout.Session.retrieve(checkout_session_id)
    print(session.amount_subtotal)
    customer = stripe.Customer.retrieve(session.customer)
    user_payment = UserPayment(
        app_user=request.user, stripe_checkout_id=checkout_session_id, payment_bool=True,amount=session.amount_subtotal/100
    )
    user=User.objects.filter(id=request.user.id)
    user.update(stripe_session=checkout_session_id)
    bookings=Booking.objects.filter(user_id=request.user.id,status=False,transaction_id=checkout_session_id)
    bookings.update(status=True)
    user_payment.save()
    # user.save()
    # print(customer)
    return render(request, "payment_successful.html", {"customer": customer})


def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return render(request, "payment_cancelled.html")


# @csrf_exempt
# def stripe_webhook(request):
# 	pass
# 	stripe.api_key = settings.STRIPE_SECRET_KEY
# 	time.sleep(10)
# 	payload = request.body
# 	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
# 	event = None
# 	try:
# 		event = stripe.Webhook.construct_event(
# 			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET_TEST
# 		)
# 	except ValueError as e:
# 		return HttpResponse(status=400)
# 	except stripe.error.SignatureVerificationError as e:
# 		return HttpResponse(status=400)
# 	if event['type'] == 'checkout.session.completed':
# 		session = event['data']['object']
# 		session_id = session.get('id', None)
# 		time.sleep(15)
# 		user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
# 		user_payment.payment_bool = True
# 		user_payment.save()
# 	return HttpResponse(status=200)
