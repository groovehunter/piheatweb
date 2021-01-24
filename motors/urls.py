from django.urls import path

from . import views
from .views import MotorListView, MotorDetailView
from .views import MainValveHistoryView, WarmwaterPumpHistoryView
from .views import control, ww_control, rules_check, rules_list


urlpatterns = [
#    path('', views.index, name='index'),

    path('', MotorListView.as_view(), name='index'),
    path('<int:pk>', MotorDetailView.as_view(), name='detail'),
    path('mainvalve', MainValveHistoryView.as_view(), name='mainvalve'),
    path('mainvalve/control', control,),
    path('ww', WarmwaterPumpHistoryView.as_view(), name='ww'),
    path('ww/control', ww_control,),
    path('rules/check', rules_check),
    path('rules/list', rules_list),
]
