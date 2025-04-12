from . import models

from datetime import datetime
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse

def get_sensor_data(request):
    return HttpResponse('hello!')

@csrf_exempt
def post_sensor_data(request):
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))

        sensor_ip = json_data['sensor_ip']
        time_executed = datetime.fromisoformat(json_data['time_executed']+'+00:00')

        sensor_logged = models.Sensor.objects.filter(sensor_ip=sensor_ip).exists()
        if not sensor_logged:
            sensor = models.Sensor(sensor_ip=sensor_ip)
            sensor.save()
        else:
            sensor = models.Sensor.objects.get(sensor_ip=sensor_ip)

        sensor.sensor_request_set.create(time_executed=time_executed)
        sensor_request = models.Sensor_Request.objects.get(time_executed=time_executed)

        datapoints = json_data['datapoints']
        for datapoint in datapoints:
            time_collected = datetime.fromisoformat(datapoint['time_collected']+'+00:00')
            temperature = datapoint['temperature']
            capacitive = datapoint['capacitive']
            sensor_request.sensor_datapoints_set.create(time_collected=time_collected, temperature=temperature, capacitive=capacitive)

        print(sensor.sensor_request_set.all())
        print(sensor_request.sensor_datapoints_set.all())

        return HttpResponse('POST SUCCESSFUL')
    return HttpResponse('NOT POST')