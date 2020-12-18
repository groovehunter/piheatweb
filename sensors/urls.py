from django.urls import path

from . import views

urlpatterns = [
#    path('', views.index, name='index'),
    path('', views.SensorListView.as_view(), name='index'),
    path('<int:pk>', views.SensorDetailView.as_view()),
    path('<int:sensor_id>/last_measures/', views.last_measures, name='last measures'),
]
