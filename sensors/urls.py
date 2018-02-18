from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),


    path('<int:sensor_id>/last_measures/', views.last_measures, name='last measures'),
]



