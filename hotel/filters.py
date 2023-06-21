
# from django_filters import FilterSet
# from django_filters.filters import RangeFilter
# from .models import Hotel
# from .forms import PriceFilterFormHelper
# from .widgets import CustomRangeWidget


# class AllRangeFilter(RangeFilter):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         values = [p.price_per_day for p in Hotel.objects.all()]
#         min_value = min(values)
#         max_value = max(values)
#         self.extra['widget'] = CustomRangeWidget(attrs={'data-range_min':min_value,'data-range_max':max_value})

# class HotelFilter(FilterSet):
#   price_per_day =AllRangeFilter()

#   class Meta:
#       model = Hotel
#       fields = ['price_per_day']
#       form=PriceFilterFormHelper