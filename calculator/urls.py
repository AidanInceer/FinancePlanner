from django.urls import path

from . import views

app_name = "calculator"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/calculate", views.calculate, name="calculate"),
    path("health", views.health_check, name="health_check"),
]
