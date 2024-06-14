from django.contrib import admin
from django.urls import path, re_path
from .views import MarkersMapView, showroute, showmap
from . import views

app_name = "mapp"
urlpatterns = [
    path("<str:lat1>/<str:long1>/<str:lat2>/<str:long2>/", showroute, name="showroute"),
    path("", showmap, name="showmap"),
]
