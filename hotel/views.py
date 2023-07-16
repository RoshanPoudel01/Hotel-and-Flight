from django.shortcuts import render, get_object_or_404
from .models import Hotel, Amnities
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from bookings.models import Booking
from flight.forms import FlightForm
from .forms import  PriceRangeForm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from .filters import HotelFilter

# Create your views here.


def homepage_view(request):
    hotel = Hotel.objects.all()
    amenity = Amnities.objects.all()
    flight_form = FlightForm(request.POST or None, request.FILES or None)
    paginator = Paginator(hotel, per_page=6)
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
        request,
        "index.html",
        {"hotel": page_obj, "amenity": amenity, "flight": flight_form},
    )


def hotel_detail_view(request, hotelid):
    hotel = get_object_or_404(Hotel, id=hotelid)
    return render(request, "hotel_detail.html", {"form": hotel})


def search_view(request):
    form = PriceRangeForm(request.GET or None)
 
    if request.method == "POST":
        searchtext = request.POST["searchtext"].title()
        searchresult = Hotel.objects.filter(
            Q(hotel_name__contains=searchtext) | Q(city__contains=searchtext)
        )
        paginator = Paginator(searchresult, per_page=6)
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
            request, "search.html", {"searchtext": searchtext, "form": page_obj,"sort":form}
        )
    else:
        return render(request, "search.html")


def sort_hotel(request):
    form = PriceRangeForm(request.GET or None)
   
    if request.method == "POST":
        searchtext = request.POST["searchtext"].title()
        hotels = Hotel.objects.filter(
            Q(hotel_name__contains=searchtext) | Q(city__contains=searchtext)
        )
        min_price = request.POST['min_price']
        max_price = request.POST['max_price']
        hotels = hotels.filter(price_per_day__gte=min_price, price_per_day__lte=max_price)
        sorted_hotels = hotels.order_by('price_per_day')
        context = {
            'sort':form,
        'hotels': sorted_hotels,
        }
        return render(request, 'sort_hotel.html', context)
    else:
        return render(request, 'search.html', {'sort': form})
    


