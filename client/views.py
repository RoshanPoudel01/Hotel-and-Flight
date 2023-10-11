from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.urls import  reverse
from django.http import HttpResponseRedirect
from .forms import HotelCreationForm, ImageForm, PhoneForm
from hotel.models import Hotel,Image,Phone
from django.http import HttpResponse
import csv
from django.contrib import messages 

from bookings.models import Booking
from payment.models import UserPayment

def user_check(user):
    return user.is_client

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def clientdashboard(request):
    user=request.user
    hotels_added_by_user = Hotel.objects.filter(added_by=user)
    hotel_count=hotels_added_by_user.count()
    if hotels_added_by_user:
         # Retrieve all bookings related to hotels added by the current user
        bookings = Booking.objects.filter(hotel__in=hotels_added_by_user)
        print(bookings)

        # Create a list to store the transaction IDs of the bookings
        transaction_ids = [booking.transaction_id for booking in bookings]
    
        # Retrieve payments related to these transaction IDs
        payments = UserPayment.objects.filter(stripe_checkout_id__in=transaction_ids)
        total_payment = sum(float(payment.amount) for payment in payments)
      
        return render(request,'dashboard.html',{'hotelcount':hotel_count,"bookingcount":bookings.count(),"totalpayment":total_payment})

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def add_hotel(request):
    form = HotelCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        usr=form.save(commit=False)
        usr.added_by= request.user
        usr.save()
        form.save_m2m()
        messages.success(request, "Hotel Added Successfully")
        return HttpResponseRedirect(reverse("client:list_hotel"))
    return render(
        request,
        "hotel_add.html",
        {"form": form},
    )

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def list_hotel(request):
    user=request.user
    hotel = Hotel.objects.filter(added_by=user)
    print(hotel)
    return render(request,'hotel_list.html',{'hotels':hotel})



@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def edit_hotel(request,hotelid):
    hotel = get_object_or_404(Hotel, id=hotelid)
    form = HotelCreationForm(request.POST or None, request.FILES or None,instance=hotel)
    if form.is_valid():
        form.save()
        messages.success(request, "Hotel Edited Successfully")
        return HttpResponseRedirect(reverse("client:list_hotel"))
    return render(request,"hotel_add.html",{"form":form})

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def delete_hotel(request):
    hotelid = request.POST.get("hotelid")
    hotel = get_object_or_404(Hotel, id=hotelid)
    hotel.delete()
    messages.success(request, "Hotel Deleted Successfully")

    return HttpResponseRedirect(reverse("client:list_hotel"))

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def add_phone(request,hotelid):
    hotel = get_object_or_404(Hotel, id=hotelid)
    form =PhoneForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        phn=form.save(commit=False)
        phn.hotel=hotel
        phn.save()
        messages.success(request, "Hotel Phone Number Added Successfully")

        return HttpResponseRedirect(reverse("client:list_hotel"))
    return render(request,"add_phone.html",{"phone":form})

def is_valid_image(file):
    # List of accepted image file formats
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    return any(file.name.lower().endswith(ext) for ext in valid_extensions)

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def add_images(request,hotelid):
   
    hotel = get_object_or_404(Hotel, id=hotelid)
    form =ImageForm(request.POST or None, request.FILES or None)
    images=request.FILES.getlist('image')
    if request.method == 'POST':
        for i in images:
            if not is_valid_image(i):
                messages.error(request, 'File type is not supported. Supported File are of type: jpg, jpeg, png, gif')
                return HttpResponseRedirect(reverse("client:add_image", kwargs={'hotelid':hotelid}))
            imag=Image.objects.create(image=i,hotel=hotel)
            imag.save()
            messages.success(request, "Hotel Image Added Successfully")

        return HttpResponseRedirect(reverse("client:list_hotel"))
    return render(request,"add_image.html",{"image":form})
    

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def list_phone(request):
    user=request.user
    hotels=Hotel.objects.filter(added_by=user)
    if hotels:
      
        phone = Phone.objects.filter(hotel__in=hotels)
        return render(request,'list_phone.html',{'phone':phone})
    
    return render(request,'list_phone.html')


@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def list_image(request):
    user=request.user
    hotel=Hotel.objects.filter(added_by=user)
    if hotel:
        image = Image.objects.filter(hotel__in=hotel)
        return render(request,'list_images.html',{'images':image})
      
    return render(request,'list_images.html')

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def delete_image(request):
    imageid = request.POST.get("hotelid")
    image = get_object_or_404(Image, id=imageid)
    image.delete()
    messages.success(request, "Hotel Image Deleted Successfully")

    return HttpResponseRedirect(reverse("client:list_image"))



@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def delete_phone(request):
    phoneid = request.POST.get("hotelid")
    phone = get_object_or_404(Phone, id=phoneid)
    phone.delete()
    messages.success(request, "Hotel Phone Number Deleted Successfully")

    return HttpResponseRedirect(reverse("client:list_phone"))


@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def list_bookings(request):
    user=request.user
    hotels = Hotel.objects.filter(added_by=user)
    
    if hotels:
        bookings = Booking.objects.filter(hotel__in=hotels)
        return render(request,'bookings.html',{'bookings':bookings})
    
    return render(request,'bookings.html')


@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def export_bookings(request):
    user=request.user
    hotels = Hotel.objects.filter(added_by=user)
    
    if hotels:
        bookings = Booking.objects.filter(hotel__in=hotels)

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="bookings.csv"'},
        )
        
        writer = csv.writer(response)
        writer.writerow(["Hotel Name", "Check In Date", "Check Out Date",])

        for booking in bookings:
            writer.writerow([ booking.hotel.hotel_name,booking.check_in_date, booking.check_out_date,])

        return response
    
@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def export_hotels(request):
    user=request.user
    hotels = Hotel.objects.filter(added_by=user)

    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="hotels.csv"'},
    )
    
    writer = csv.writer(response)
    writer.writerow(["Hotel Name", "Email", "City","Price Per Day"])

    for hotel in hotels:
        writer.writerow([ hotel.hotel_name, hotel.email,hotel.city,hotel.price_per_day])
    return response






@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def list_payments(request):
    user=request.user
    hotels_added_by_user = Hotel.objects.filter(added_by=user)
    if hotels_added_by_user:
         # Retrieve all bookings related to hotels added by the current user
        bookings = Booking.objects.filter(hotel__in=hotels_added_by_user)

        # Create a list to store the transaction IDs of the bookings
        transaction_ids = [booking.transaction_id for booking in bookings]
    
        # Retrieve payments related to these transaction IDs
        payments = UserPayment.objects.filter(stripe_checkout_id__in=transaction_ids)
    
   
    
    return render(request,'payment.html',{'payments': payments})


@login_required
@user_passes_test(user_check,redirect_field_name="client:list_payments")
def export_payments(request):
    user=request.user
    hotels_added_by_user = Hotel.objects.filter(added_by=user)
    if hotels_added_by_user:
         # Retrieve all bookings related to hotels added by the current user
        bookings = Booking.objects.filter(hotel__in=hotels_added_by_user)

        # Create a list to store the transaction IDs of the bookings
        transaction_ids = [booking.transaction_id for booking in bookings]
    
        # Retrieve payments related to these transaction IDs
        payments = UserPayment.objects.filter(stripe_checkout_id__in=transaction_ids)
    
   
        response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="payment.csv"'},
    )
    
        writer = csv.writer(response)
        writer.writerow(["Amount", "Paid Date", "Updated Date","Status"])

        for payment in payments:
            writer.writerow([payment.amount, payment.created_at,payment.modified_at,payment.payment_bool])
        return response
