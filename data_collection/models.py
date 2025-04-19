from django.db import models

# Create your models here.
class Sensor(models.Model):
    sensor_ip = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.sensor_ip

class Sensor_Request(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    time_executed = models.DateTimeField()
    def __str__(self):
        sensor_ip = Sensor.objects.get(id=self.sensor_id).sensor_ip
        return sensor_ip + ", requested at " + self.time_executed.ctime()


class Sensor_Datapoints(models.Model):
    sensor_request = models.ForeignKey(Sensor_Request, on_delete=models.CASCADE)
    time_collected = models.DateTimeField()
    temperature = models.FloatField()
    capacitive = models.FloatField()
    def __str__(self):
        sensor_id = Sensor_Request.objects.get(id=self.sensor_request_id).sensor_id
        sensor_ip = Sensor.objects.get(id=sensor_id).sensor_ip
        return sensor_ip + ", collected at " + self.time_collected.ctime() + "\nTemperature: " + str(self.temperature) + "\nCapacitive" + str(self.capacitive)

