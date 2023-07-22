from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.urls import  reverse
from django.http import HttpResponseRedirect
from .forms import HotelCreationForm, ImageForm, PhoneForm
from hotel.models import Hotel,Image,Phone

from bookings.models import Booking

def user_check(user):
    return user.is_client

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def clientdashboard(request):
    hotel=Hotel.objects.filter(added_by=request.user)
    return render(request,'dashboard.html',{'hotells':hotel})

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def add_hotel(request):
    form = HotelCreationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        usr=form.save(commit=False)
        print(request.user.id)
        usr.added_by= request.user
        usr.save()
        return HttpResponseRedirect(reverse("client:clientdashboard"))
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
        return HttpResponseRedirect(reverse("client:list_hotel"))
    return render(request,"hotel_add.html",{"form":form})

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def delete_hotel(request):
    hotelid = request.POST.get("hotelid")
    hotel = get_object_or_404(Hotel, id=hotelid)
    hotel.delete()
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
        return HttpResponseRedirect(reverse("client:list_hotel"))
    return render(request,"add_phone.html",{"phone":form})

@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def add_images(request,hotelid):
    hotel = get_object_or_404(Hotel, id=hotelid)
    form =ImageForm(request.POST or None, request.FILES or None)
    images=request.FILES.getlist('image')
    if form.is_valid() :
        for i in images:
            imag=Image.objects.create(image=i,hotel=hotel)
            imag.save()
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
    return HttpResponseRedirect(reverse("client:list_image"))



@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def delete_phone(request):
    phoneid = request.POST.get("hotelid")
    phone = get_object_or_404(Phone, id=phoneid)
    phone.delete()
    return HttpResponseRedirect(reverse("client:list_phone"))


@login_required
@user_passes_test(user_check,redirect_field_name="hotel:homepage")
def list_bookings(request):
    user=request.user
    hotels = Hotel.objects.filter(added_by=user)
    print(hotels)
    if hotels:
        bookings = Booking.objects.filter(hotel__in=hotels)
        return render(request,'bookings.html',{'bookings':bookings})
    
    return render(request,'bookings.html')


