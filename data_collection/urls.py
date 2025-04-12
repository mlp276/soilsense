from django.urls import path

from . import parse_requests

urlpatterns = [
    path("get/", parse_requests.get_sensor_data, name="getsensordata"),
    path("post/", parse_requests.post_sensor_data, name="postsensordata")
]