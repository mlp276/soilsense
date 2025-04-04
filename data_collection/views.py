from django.shortcuts import render

import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
def get_sensor_data(request):
    return HttpResponse("hello!")

@csrf_exempt
def post_sensor_data(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        print(json.dumps(json_data, indent=4, separators=(", ", " = ")))
        return HttpResponse("Post successful")
    return HttpResponse("Not Post")