from django.shortcuts import render

import requests
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
def get_sensor_data(request):
    url = 'http://example.com'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return HttpResponse(response.content)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error", str(e)}, status=500)

    