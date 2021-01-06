from django.urls import path

from . import views
from .views import MotorListView, MotorDetailView, MainValveHistoryView
from .views import control


urlpatterns = [
#    path('', views.index, name='index'),

    path('', MotorListView.as_view(), name='index'),
    path('<int:pk>', MotorDetailView.as_view(), name='detail'),
    path('mainvalve', MainValveHistoryView.as_view(), name='mainvalve'),
    path('mainvalve/control', control,)
]
