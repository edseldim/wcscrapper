from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('results-<str:date_data>', views.return_hello_world, name="hello_world"),
]