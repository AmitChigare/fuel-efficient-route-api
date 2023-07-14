from django.shortcuts import render, redirect
from .models import School
from django.core.paginator import Paginator
import math
import random
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="FuelEfficientRoutesApp")

def fuel_efficient_route2(request, pincode, latitude, longitude):
    origin = (latitude, longitude)
    if latitude==0.0 and longitude==0.0:
        origin_name='Location Unavailable'
    else:
        origin_name = get_location_name(latitude, longitude)

    schools = School.objects.filter(pin_code=pincode)
    distances = []

    for school in schools:
        destination = (school.latitude, school.longitude)
        dist = round(geodesic(origin, destination).km, 1)
        distances.append((school, dist))

    distances.sort(key=lambda x: x[1])

    #Pagination
    paginator=Paginator(distances, 10)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    context = {
        "pincode": pincode,
        "origin_name": origin_name,
        "page_obj": page_obj,
    }
    return render(request, "fuel_efficient_route.html", context) 

def fuel_efficient_route(request):
    if request.method == "POST":
        pincode = request.POST.get("pincode")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        print(latitude, longitude)
        if not latitude or not longitude:
            latitude=0.0
            longitude=0.0
        return redirect('fuel_efficient_route2', pincode=pincode, latitude=latitude, longitude=longitude)

    return render(request, "fuel_efficient_form.html")


def get_location_name(latitude, longitude):
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location:
        return location.address
    else:
        return None
