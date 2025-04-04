from django.db import models

# Create your models here.
class Sensor(models.Model):
    sensor_id = models.IntegerField(primary_key=True, unique=True)
    sensor_ip = models.CharField(max_length=255)

class Sensor_Request(models.Model):
    request_id = models.IntegerField(primary_key=True, unique=True)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    time_executed = models.DateTimeField()

class Sensor_Datapoints(models.Model):
    data_id = models.IntegerField(primary_key=True, unique=True)
    sensor_id = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    time_collected = models.DateTimeField()
    temperature = models.FloatField()
    capacitive = models.FloatField()
