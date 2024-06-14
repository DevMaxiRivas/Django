# Create your views here.
from django.shortcuts import render
import pandas as pd
from django.templatetags.static import static
from django.http import JsonResponse


def chart_data(request):
    df = pd.read_csv("dashboard/static/car_sales.csv")
    rs = df.groupby("Engine_size")["Sales_in_thousands"].agg("sum")
    categories = list(rs.index)
    values = list(rs.values)
    chart_data = {
        "label": "Line Chart",
        "labels": categories,
        "values": values,
        "chart_type": "bar",
    }
    return JsonResponse(chart_data)


def chart_view(request):
    return render(request, "chart.html", {})
