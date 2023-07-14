from django.urls import path
from .views import fuel_efficient_route

urlpatterns = [
    path("", fuel_efficient_route, name="fuel_efficient_route"),
    # path("school_list/", school_list, name="school_list"),
]
