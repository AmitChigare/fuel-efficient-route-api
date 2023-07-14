from django.shortcuts import render
from .models import School
import math
import random
from geopy.distance import geodesic


def calculate_distance(coord1, coord2):
    # Calculate distance using Haversine formula or any other distance calculation method
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    radius = 6371  # Earth's radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(
        math.radians(lat1)
    ) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance


def school_list(request):
    if request.method == "POST":
        pin_code = request.POST.get("pin_code")
        schools = School.objects.filter(pin_code=pin_code)

        # Create a dictionary to store school coordinates
        coordinates = {}
        for school in schools:
            coordinates[school.id] = (school.latitude, school.longitude)

        # Create a dictionary to store distances
        distances = {}

        # Find the distances between schools
        for school_id in coordinates:
            for other_school_id in coordinates:
                if school_id != other_school_id:
                    distance = calculate_distance(
                        coordinates[school_id], coordinates[other_school_id]
                    )
                    distances[(school_id, other_school_id)] = distance

        print(distances)

        # Sort the distances by shortest distance
        sorted_distances = sorted(distances.items(), key=lambda x: x[1])

        # Display the distances
        for (school_id_1, school_id_2), distance in sorted_distances:
            school_1 = School.objects.get(id=school_id_1)
            school_2 = School.objects.get(id=school_id_2)
            print(
                f"Distance between {school_1.name} and {school_2.name}: {distance} units"
            )
        return render(request, "school_list.html")

        #################################################################
        # Create a dictionary to store school coordinates
        # coordinates = {}
        # for school in schools:
        #     coordinates[school.id] = (school.latitude, school.longitude)

        # # Initialize variables
        # unvisited_schools = set(coordinates.keys())
        # current_school = next(iter(unvisited_schools))
        # visited_schools = [current_school]

        # # Find the nearest school and add it to the route until all schools are visited
        # while unvisited_schools:
        #     next_school = None
        #     min_distance = float("inf")

        #     for school_id in unvisited_schools:
        #         # Calculate distance between current school and the next unvisited school
        #         distance = calculate_distance(
        #             coordinates[current_school], coordinates[school_id]
        #         )

        #         if distance < min_distance:
        #             min_distance = distance
        #             next_school = school_id

        #     current_school = next_school
        #     unvisited_schools.remove(current_school)
        #     visited_schools.append(current_school)
        #     print(f"d: {distance}")

        # # Retrieve schools in the order of visit
        # ordered_schools = School.objects.filter(id__in=visited_schools).order_by("id")

        # return render(request, "school_list.html", {"schools": ordered_schools})

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
    return render(request, "school_form.html")


def fuel_efficient_route(request):
    if request.method == "POST":
        pincode = request.POST.get("pincode")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        print(pincode, latitude, longitude)

        # Set the origin coordinates based on user's location
        origin = (latitude, longitude)

        schools = School.objects.filter(pin_code=pincode)
        distances = []

        for school in schools:
            destination = (school.latitude, school.longitude)
            dist = geodesic(origin, destination).km
            distances.append((school, dist))

        distances.sort(key=lambda x: x[1])  # Sort distances in ascending order

        context = {
            "pincode": pincode,
            "schools": distances,
        }
        return render(request, "fuel_efficient_route.html", context)
    else:
        return render(request, "fuel_efficient_form.html")
