from . import models
import pandas as pd
import json
from datetime import datetime
from . import process_data
from django.db.models import Avg

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse

def get_sensor_data(request):
    if request.method == 'GET':
        sensor_ip = request.GET.get('sensor_ip', default='')

        if len(sensor_ip) == 0:
            return HttpResponse('INVALID QUERY')
        
        sensor_id = models.Sensor.objects.get(sensor_ip=sensor_ip).id
        sensor_requests = models.Sensor_Request.objects.filter(sensor_id=sensor_id)
        
        time_executed_array = []
        temperatures = []
        capacitives = []

        for sensor_request in sensor_requests:
            sensor_request_id = sensor_request.id
            datapoints = models.Sensor_Datapoints.objects.filter(sensor_request_id=sensor_request_id)
            
            time_executed = sensor_request.time_executed.isoformat()
            avg_temperature = datapoints.aggregate(Avg("temperature"))['temperature__avg']
            avg_capacitive = datapoints.aggregate(Avg("capacitive"))['capacitive__avg']

            time_executed_array.append(time_executed)
            temperatures.append(avg_temperature)
            capacitives.append(avg_capacitive)

        df = pd.DataFrame(data={'Time Collected': time_executed, 'Temperature': temperatures, 'Capacitive': capacitives})
        processed_sensordata = process_data.processData(df=df).to_dict(orient='list')

        return JsonResponse(processed_sensordata)
    return HttpResponse('NOT GET')

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