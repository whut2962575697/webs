# -*- encoding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import json
import arcpy
import xlrd

# Create your views here.


def get_bmap_boundary(request):
    city = request.GET.get("city")
    return render(request, "common/get_baidu_boundary.html", {"city": city})


def translate_coord_2_mc(request):
    coords = request.GET.get("coords")

    url = "http://api.map.baidu.com/geoconv/v1/?coords="+coords+"&from=5&to=6" \
          "&ak=BF0Y5lHmGGMReuSFBBldFOyWjEuRgdpO"
    result = {
        "status": "1"
    }
    page = requests.get(url).text
    if page:
        return HttpResponse(page, content_type="application/json")
    else:
        return HttpResponse(json.dumps(result), content_type="application/json")


@csrf_exempt
def download_shp_file(request):
    boundaries = request.POST.get("boundaries")
    boundaries = boundaries.strip("*&")
    city = request.POST.get("city")
    arcpy.env.workspace = "temp"
    wkt = "POLYGON("
    for boundary in boundaries.split("*&"):
        wkt = wkt + "("
        wkt = wkt + boundary.replace(", ", " ")
        wkt = wkt.replace(";", ",")
        wkt = wkt.strip(",")
        wkt = wkt + "),"
    wkt = wkt.strip(",") + ")"
    print (wkt)
    polygons = arcpy.FromWKT(wkt)
    if not arcpy.Exists(r'G:\xin.data\spiders_data\hbs'+"\\"+city+".shp"):
        arcpy.CopyFeatures_management(polygons, r'G:\xin.data\spiders_data\hbs'+"\\"+city+".shp")
    result = {
        "status": "0"
    }
    return HttpResponse(json.dumps(result), content_type="application/json")









