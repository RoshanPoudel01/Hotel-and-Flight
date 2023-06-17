from django.shortcuts import render, get_object_or_404
from .models import Hotel, Amnities
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from flight.forms import FlightForm
from .forms import HotelCreationForm, ImageForm, PhoneForm
from .filters import HotelFilter

# Create your views here.
def add_hotel(request):
    form = HotelCreationForm(request.POST or None, request.FILES or None)
    # imgform = ImageForm(request.POST or None, request.FILES or None)
    # phoneform = PhoneForm(request.POST or None)
    # if form.is_valid() and imgform.is_valid() and phoneform.is_valid():
    if form.is_valid():
        form.save(commit=False)
        # imgform.save(commit=False)
        # phoneform.save(commit=False)
        # messages.add_message(request, messages.INFO, "Hotel added successfully.")
        return HttpResponseRedirect(reverse("hotel:add_phone"))
    return render(
        # request, "hotel_add.html", {"form": form, "image": imgform, "phone": phoneform}
        request,
        "hotel_add.html",
        {"form": form},
    )

def add_phone(request):
    # hotel = get_object_or_404(Hotel, id=hotelid)
    form =PhoneForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(commit=False)
        return HttpResponseRedirect(reverse("hotel:add_images"))
    return render(request,"phoneadd.html",{"phone":form})

def add_images(request):
    # hotel = get_object_or_404(Hotel, id=hotelid)
    form =ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(commit=False)
        return HttpResponseRedirect(reverse("hotel:homepage"))
    return render(request,"imageadd.html",{"image":form})
def homepage_view(request):
    hotel = Hotel.objects.all()
    amenity = Amnities.objects.all()
    flight_form = FlightForm(request.POST or None, request.FILES or None)
    return render(
        request,
        "index.html",
        {"hotel": hotel, "amenity": amenity, "flight": flight_form},
    )


def hotel_detail_view(request, hotelid):
    hotel = get_object_or_404(Hotel, id=hotelid)
    return render(request, "hotel_detail.html", {"form": hotel})


def search_view(request):
    price_filter = HotelFilter(request.GET)
    if request.method == "POST":
        searchtext = request.POST["searchtext"].title()
        searchresult = Hotel.objects.filter(
            Q(hotel_name__contains=searchtext) | Q(city__contains=searchtext)
        )
        paginator = Paginator(searchresult, per_page=4)
        page_number = request.GET.get("page")
        try:
            page_obj = paginator.get_page(
                page_number
            )  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = paginator.page(paginator.num_pages)
        return render(
            request, "search.html", {"searchtext": searchtext, "form": page_obj,'price_filter':price_filter}
        )
    else:
        return render(request, "search.html")
