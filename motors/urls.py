from django.urls import path

from . import views
from .views import MotorListView, MotorDetailView


urlpatterns = [
#    path('', views.index, name='index'),

    path('', MotorListView.as_view(), name='index'),
    path('<int:pk>', MotorDetailView.as_view(), name='detail'),

]
