from django.urls import path
from dashboard import views

urlpatterns = [
    path("data/", views.chart_data, name="chart_data"),
    path("", views.chart_view, name="chart_view"),
]
