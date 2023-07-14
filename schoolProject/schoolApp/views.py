from django.shortcuts import render
from .models import School
import math
import random
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="FuelEfficientRoutesApp")


def fuel_efficient_route(request):
    # pin_codes = []
    # for i in range(150):
    #     if i % 7 == 0:
    #         # Generate a new random pin code if a multiple of 10 is encountered
    #         pin_code = str(random.randint(100000, 999999))
    #     pin_codes.append(pin_code)

    # for pin_code in pin_codes:
    #     school = {
    #         "name": f"School Name {random.randint(1, 500)}",
    #         "address": f"Address {random.randint(1, 500)} A {random.randint(1, 500)}FUG{random.randint(1, 500)}WI IWOJOI ",
    #         "pin_code": pin_code,
    #         "latitude": random.uniform(-90, 90),
    #         "longitude": random.uniform(-180, 180),
    #     }
    #     School.objects.create(**school)
    if request.method == "POST":
        pincode = request.POST.get("pincode")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        origin = (latitude, longitude)
        origin_name = get_location_name(latitude, longitude)

        schools = School.objects.filter(pin_code=pincode)
        distances = []

        for school in schools:
            destination = (school.latitude, school.longitude)
            dist = round(geodesic(origin, destination).km, 1)
            distances.append((school, dist))

        distances.sort(key=lambda x: x[1])

        context = {
            "pincode": pincode,
            "origin_name": origin_name,
            "schools": distances,
        }
        return render(request, "fuel_efficient_route.html", context)
    else:
        return render(request, "fuel_efficient_form.html")


def get_location_name(latitude, longitude):
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location:
        return location.address
    else:
        return None
