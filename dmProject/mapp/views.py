from django.views.generic.base import TemplateView
import folium
from django.shortcuts import render, redirect
from .utils import get_route


class MarkersMapView(TemplateView):
    template_name = "map.html"


def showmap(request):
    return render(request, "showMap.html")


def showroute(request, lat1, long1, lat2, long2):
    figure = folium.Figure()
    lat1, long1, lat2, long2 = float(lat1), float(long1), float(lat2), float(long2)

    route = get_route(long1, lat1, long2, lat2)

    m = folium.Map(location=[lat1, long1], zoom_start=10)
    m.add_to(figure)

    folium.PolyLine(route["route"], weight=8, color="blue", opacity=0.6).add_to(m)
    folium.Marker(
        location=[lat1, long1], icon=folium.Icon(icon="play", color="green")
    ).add_to(m)
    folium.Marker(
        location=[lat2, long2], icon=folium.Icon(icon="stop", color="red")
    ).add_to(m)

    figure.render()
    context = {"map": figure}

    return render(request, "showRoute.html", context)
