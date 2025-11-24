from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # still cache the final response for 15 minutes if required
def property_list(request):
    properties = get_all_properties()
    return JsonResponse({
        "data": properties
    })
