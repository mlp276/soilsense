from django.urls import path

from . import parse_requests

urlpatterns = [
    path("retrieve/", parse_requests.get_sensor_data, name="getsensordata"),
    path("collect/", parse_requests.post_sensor_data, name="postsensordata")
]