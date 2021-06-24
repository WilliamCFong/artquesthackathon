from django.urls import path
from city_resource import api

urlpatterns = [
    path("city_resource/<str:slug>/", api.city_datasource, name="city_resource"),
]
