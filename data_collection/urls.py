from django.urls import path

from . import views

urlpatterns = [
    path("get/", views.get_sensor_data, name="getsensordata"),
    path("post/", views.post_sensor_data, name="postsensordata")
]