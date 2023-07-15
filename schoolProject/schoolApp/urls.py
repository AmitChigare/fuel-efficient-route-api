from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    # path("fuel_efficient_route2/<str:pincode>/<float:latitude>/<float:longitude>/", fuel_efficient_route2, name="fuel_efficient_route2"),
    re_path(
        r"^fuel_efficient_route/(?P<pincode>\w+)/(?P<latitude>[-+]?\d*\.\d+)/(?P<longitude>[-+]?\d*\.\d+)/$",
        fuel_efficient_route,
        name="fuel_efficient_route",
    ),
]
