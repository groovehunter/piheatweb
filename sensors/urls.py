from django.urls import path

from . import views

urlpatterns = [
#    path('', views.index, name='index'),
    path('', views.SensorListView.as_view(), name='index'),
    path('<int:pk>', views.SensorDetailView.as_view()),
    #path('<int:sid>', views.data(action='list'),
    path('<int:sid>/data/<str:action>', views.data),
    path('view/<str:action>', views.data2),
]
